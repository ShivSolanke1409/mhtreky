from django.db import models
from accounts.models import OrganizerProfile
from django.conf import settings
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL

class Camp(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending approval"
        APPROVED = "approved", "Approved"
        DISABLED = "disabled", "Disabled"

    organizer = models.ForeignKey(
        OrganizerProfile,
        on_delete=models.CASCADE,
        related_name="camps"
    )

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    cover_image = models.ImageField(upload_to="camps/cover/")
    is_featured = models.BooleanField(default=False)
    featured_order = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CampImage(models.Model):
    camp = models.ForeignKey(
        Camp,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="camps/gallery/")

    def __str__(self):
        return f"Image for {self.camp.name}"


class CampPricing(models.Model):
    camp = models.ForeignKey(
        Camp,
        on_delete=models.CASCADE,
        related_name="pricing"
    )
    date = models.DateField()
    price_per_person = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("camp", "date")
        ordering = ["date"]

    def __str__(self):
        return f"{self.camp.name} - {self.date}"


class CampAvailability(models.Model):
    camp = models.ForeignKey(
        Camp,
        on_delete=models.CASCADE,
        related_name="availability"
    )
    date = models.DateField()
    available_slots = models.PositiveIntegerField()

    class Meta:
        unique_together = ("camp", "date")

    def __str__(self):
        return f"{self.camp.name} - {self.date}"

