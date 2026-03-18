from django.contrib import admin
from .models import Camp, CampImage, CampPricing, CampAvailability


@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'is_featured', 'featured_order')
    list_filter = ('is_featured', 'status')
    search_fields = ('name', 'location')
    list_editable = ('is_featured', 'featured_order')
    ordering = ('featured_order',)


admin.site.register(CampImage)
admin.site.register(CampPricing)
admin.site.register(CampAvailability)