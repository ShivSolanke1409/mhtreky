from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User, OrganizerProfile


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            if user.is_organizer:
                return redirect("dashboard:home")

            return redirect("camps:home")

        messages.error(request, "Invalid email or password")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("camps:home")


def register_customer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        user = User.objects.create_user(
            email=email,
            phone=phone,
            password=password,
        )
        user.is_customer = True
        user.save()

        login(request, user)
        return redirect("camps:home")

    return render(request, "accounts/register_customer.html")


def register_organizer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        org_name = request.POST.get("organization_name")
        contact_person = request.POST.get("contact_person")

        user = User.objects.create_user(
            email=email,
            phone=phone,
            password=password,
        )
        user.is_organizer = True
        user.save()

        OrganizerProfile.objects.create(
            user=user,
            organization_name=org_name,
            contact_person=contact_person,
            phone=phone,
        )

        login(request, user)
        return redirect("dashboard:home")

    return render(request, "accounts/register_organizer.html")
