from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
  
    path("bookings/<int:camp_id>/book/", views.create_booking, name="create_booking"),
    path("booking/<int:booking_id>/", views.booking_summary, name="booking_summary"),

]