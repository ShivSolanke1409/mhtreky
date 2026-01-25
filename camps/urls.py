from django.urls import path
from . import views

app_name = "camps"

urlpatterns = [
    path("", views.home, name="home"),
    path("camps/", views.camp_list, name="camp_list"),
    path("camps/<int:id>/", views.camp_detail, name="camp_detail"),
    path("camps/<int:camp_id>/book/", views.create_booking, name="create_booking"),
    path("booking/<int:booking_id>/", views.booking_summary, name="booking_summary"),

]
