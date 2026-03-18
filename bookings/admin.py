from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'camp', 'date', 'people_count', 'status', 'created_at')
    list_filter = ('status', 'date', 'camp')
    search_fields = ('user__username', 'camp__name')
