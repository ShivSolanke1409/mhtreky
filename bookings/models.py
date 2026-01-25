from django.db import models
from django.conf import settings
from camps.models import Camp

class Booking(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'is_customer': True}
    )

    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    date = models.DateField()
    people_count = models.PositiveIntegerField()

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.camp.name} - {self.user.email}"
