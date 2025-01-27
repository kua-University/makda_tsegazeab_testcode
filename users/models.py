# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# class User(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.username
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    age = models.PositiveIntegerField(null=True, blank=True)  # Add age field

    def __str__(self):
        return self.username