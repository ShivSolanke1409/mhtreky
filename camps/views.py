from django.core.paginator import Paginator
from django.db.models import Min, Q
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Camp, CampPricing, CampAvailability, CampBooking
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, "camps/home.html")

def camp_list(request):
    location = request.GET.get("location", "").strip()
    page_number = request.GET.get("page", 1)

    today = now().date()
    last_day = today + timedelta(days=30)

    base_qs = (
        Camp.objects
        .filter(
            status=Camp.Status.APPROVED,
            pricing__date__range=(today, last_day),
            pricing__is_available=True,
            availability__date__range=(today, last_day),
            availability__available_slots__gt=0,
        )
        .annotate(
            starting_price=Min(
                "pricing__price_per_person",
                filter=Q(
                    pricing__date__range=(today, last_day),
                    pricing__is_available=True,
                )
            )
        )
        .filter(starting_price__isnull=False)
        .distinct()
        .order_by("starting_price", "-created_at")
    )

    if location:
        base_qs = base_qs.filter(location__icontains=location)

    paginator = Paginator(base_qs, 9)  # 9 camps per page
    camps = paginator.get_page(page_number)

    return render(
        request,
        "camps/camp_list.html",
        {
            "camps": camps,
            "location": location,
        }
    )

def camp_detail(request, id):
    today = now().date()
    last_day = today + timedelta(days=30)

    camp = get_object_or_404(
        Camp,
        id=id,
        status=Camp.Status.APPROVED
    )

    pricing = (
        CampPricing.objects
        .filter(
            camp=camp,
            date__range=(today, last_day)
        )
        .order_by("date")
    )

    availability = {
        a.date: a.available_slots
        for a in CampAvailability.objects.filter(
            camp=camp,
            date__range=(today, last_day),
            available_slots__gt=0
        )
    }

    # Merge pricing + availability
    date_data = []
    for p in pricing:
        slots = availability.get(p.date, 0)
        date_data.append({
            "date": p.date,
            "price": p.price_per_person,
            "slots": slots,
            "is_available": slots > 0
        })

    return render(
        request,
        "camps/camp_detail.html",
        {
            "camp": camp,
            "date_data": date_data,
        }
    )

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

    return redirect("camps:booking_summary", booking_id=booking.id)

@login_required
def booking_summary(request, booking_id):
    booking = get_object_or_404(
        CampBooking,
        id=booking_id,
        user=request.user
    )

    return render(
        request,
        "camps/booking_summary.html",
        {"booking": booking}
    )
