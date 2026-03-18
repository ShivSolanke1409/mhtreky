from django.core.paginator import Paginator
from django.db.models import Min, Q
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Camp, CampPricing, CampAvailability
from django.db import transaction
from django.contrib.auth.decorators import login_required  
from django.contrib import messages


def home(request):
    featured_camps = Camp.objects.filter(
        is_featured=True,
        status=Camp.Status.APPROVED
    ).order_by('featured_order')[:8]

    return render(request, 'camps/home.html', {
        'featured_camps': featured_camps
    })

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
    camp = get_object_or_404(Camp, id=id)

    today = timezone.localdate()
    next_30_days = today + timedelta(days=30)

    availability = CampAvailability.objects.filter(
        camp=camp,
        date__gte=today,
        date__lte=next_30_days,
        available_slots__gt=0
    ).order_by("date")

    pricing = CampPricing.objects.filter(
        camp=camp,
        date__gte=today
    ).order_by("date")

    starting_price = (
        pricing.first().price_per_person
        if pricing.exists()
        else None
    )

    context = {
        "camp": camp,
        "gallery": camp.images.all(),
        "availability": availability,
        "pricing": pricing,
        "starting_price": starting_price,
    }

    return render(request, "camps/camp_detail.html", context)


