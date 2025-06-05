from datetime import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
