from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('analyst', 'Analyst'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class ClimateDataset(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    file = models.FileField(upload_to='datasets/')
    upload_date = models.DateTimeField(auto_now_add=True)
