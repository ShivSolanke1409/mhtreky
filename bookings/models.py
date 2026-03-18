from django.db import models
from django.conf import settings  # import settings
from camps.models import Camp, CampAvailability

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    date = models.DateField()
    people_count = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_amounts(self, price_per_person):
        self.subtotal = price_per_person * self.people_count
        self.service_fee = self.subtotal * 0.05
        self.total_amount = self.subtotal + self.service_fee
        self.advance_amount = self.total_amount * 0.3
        self.balance_amount = self.total_amount - self.advance_amount

    def __str__(self):
        return f"{self.user} - {self.camp} - {self.date}"
