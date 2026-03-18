from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, datetime

from camps.models import Camp, CampPricing, CampAvailability
from .models import Booking


@login_required
def book_camp(request, camp_id):
    camp = get_object_or_404(Camp, id=camp_id)
    
    print("POST DATA:", request.POST)
    if request.method == "POST":
        
        date = request.POST.get("date")
        people_count = request.POST.get("people_count")

        if not date or not people_count:
            messages.error(request, "Missing booking data.")
            return redirect("camps:camp_detail", id=camp.id)

        try:
            people_count = int(people_count)
           
            if people_count <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Invalid input values.")
            return redirect("camps:camp_detail", id=camp.id)

        with transaction.atomic():

            availability = CampAvailability.objects.select_for_update().filter(
                camp=camp,
                date=date
            ).first()

            if not availability or availability.available_slots < people_count:
                messages.error(request, "Not enough slots available.")
                return redirect("camps:camp_detail", id=camp.id)

            pricing = CampPricing.objects.filter(
                camp=camp,
                date=date,
                is_available=True
            ).first()

            if not pricing:
                messages.error(request, "Pricing not available.")
                return redirect("camps:camp_detail", id=camp.id)

            booking = Booking(
                user=request.user,
                camp=camp,
                date=date,
                people_count=people_count,
                status="pending"
            )

            booking.calculate_amounts(pricing.price_per_person)
            booking.save()
            availability.available_slots -= people_count
            availability.save()

        messages.success(request, "Booking created successfully.")
        return redirect("bookings:booking_success", booking_id=booking.id)

    return render(request, "bookings/book_camp.html", {
        "camp": camp,
    })


@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_success.html', {'booking': booking})


@login_required
def booking_summary(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_summary.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


# 🔥 PROPER CANCEL LOGIC
@login_required
@transaction.atomic
def cancel_booking(request, booking_id):

    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    booking = get_object_or_404(
        Booking.objects.select_for_update(),
        id=booking_id,
        user=request.user
    )

    # Already cancelled
    if booking.status == "cancelled":
        messages.warning(request, "This booking is already cancelled.")
        return redirect("bookings:booking_summary", booking_id=booking.id)

    # ❌ Block if within 48 hours
    camp_datetime = timezone.make_aware(
        datetime.combine(booking.date, datetime.min.time())
    )

    if camp_datetime - timezone.now() < timedelta(hours=48):
        messages.error(
            request,
            "Cancellation not allowed within 48 hours of camp date."
        )
        return redirect("bookings:booking_summary", booking_id=booking.id)

    # ❌ Block if fully paid and confirmed
    if booking.status == "confirmed" and booking.balance_amount == 0:
        messages.error(
            request,
            "Fully paid confirmed bookings cannot be cancelled."
        )
        return redirect("bookings:booking_summary", booking_id=booking.id)

    # Restore availability
    availability = CampAvailability.objects.filter(
        camp=booking.camp,
        date=booking.date
    ).first()

    if availability:
        availability.available_slots += booking.people_count
        availability.save()

    booking.status = "cancelled"
    booking.save()

    messages.success(request, "Booking cancelled successfully.")

    return redirect("bookings:booking_summary", booking_id=booking.id)