from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path('book/<int:camp_id>/', views.book_camp, name='book_camp'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking-summary/<int:booking_id>/', views.booking_summary, name='booking_summary'),  # ✅ added summary URL
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
