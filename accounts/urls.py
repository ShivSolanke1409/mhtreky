from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_customer, name="register_customer"),
    path("register-organizer/", views.register_organizer, name="register_organizer"),
    path("logout/", views.logout_view, name="logout")
]
