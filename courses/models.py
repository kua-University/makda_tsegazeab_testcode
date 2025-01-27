from django.db import models
from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    credit_hour = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return self.name
