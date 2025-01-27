from django.db import models
from registration.models import Registration


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    available_slots = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


class Payment(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')  # Pending, Completed, Failed

    def __str__(self):
        return f'Payment for {self.registration.student.username} - {self.amount} ({self.status})'
