from django.contrib import admin

# Register your models here.
from .models import Camp, CampImage, CampPricing, CampAvailability, CampBooking

admin.site.register(Camp)
admin.site.register(CampImage)
admin.site.register(CampPricing)
admin.site.register(CampAvailability)
admin.site.register(CampBooking)