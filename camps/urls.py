from django.urls import path
from . import views

app_name = "camps"

urlpatterns = [
    path("", views.home, name="home"),
    path("camps/", views.camp_list, name="camp_list"),
    path("camps/<int:id>/", views.camp_detail, name="camp_detail"),


]
