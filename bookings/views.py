from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from camps.models import Camp, CampAvailability, CampPricing, CampBooking
from django.db import transaction
from django.contrib import messages
# Create your views here.
@login_required
def create_booking(request, camp_id):
    if request.method != "POST":
        return redirect("camps:camp_detail", camp_id=camp_id)

    date = request.POST.get("date")
    guests = int(request.POST.get("guests", 1))

    camp = get_object_or_404(
        Camp,
        id=camp_id,
        status=Camp.Status.APPROVED
    )

    with transaction.atomic():

        availability = (
            CampAvailability.objects
            .select_for_update()
            .get(camp=camp, date=date)
        )

        if availability.available_slots < guests:
            messages.error(request, "Not enough slots available.")
            return redirect("camps:camp_detail", camp_id=camp.id)

        pricing = CampPricing.objects.get(
            camp=camp,
            date=date,
            is_available=True
        )

        total_amount = pricing.price_per_person * guests

        booking = CampBooking.objects.create(
            user=request.user,
            camp=camp,
            date=date,
            guests=guests,
            price_per_person=pricing.price_per_person,
            total_amount=total_amount,
            status=CampBooking.Status.PENDING,
        )

        availability.available_slots -= guests
        availability.save()

    return redirect("bookings:booking_summary", booking_id=booking.id)

@login_required
def booking_summary(request, booking_id):
    booking = get_object_or_404(
        CampBooking,
        id=booking_id,
        user=request.user
    )

    return render(
        request,
        "bookings/booking_summary.html",
        {"booking": booking}
    )
