from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('business', 'Business'),
        ('both', 'Both'),
    ]
    user = models.OneToOneField(User, on_index=True, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    profession = models.CharField(max_length=10, choices=ROLE_CHOICES)
    raw_material_info = models.TextField(help_text="What do you have or what do you need?")

    def __str__(self):
        return f"{self.user.username} - {self.profession}"