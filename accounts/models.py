from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    father_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username
