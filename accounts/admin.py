from django.contrib import admin
from django.contrib.auth.models import User
from .models import OrganizerProfile, User


admin.site.register(User)
admin.site.register(OrganizerProfile)
