from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Matches your requirement for three choices
    PROFESSION_CHOICES = [
        ('farmer', 'Farmer'),
        ('business', 'Business'),
        ('both', 'Both'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=10, choices=PROFESSION_CHOICES)
    # This captures what they have or what they want
    material_details = models.TextField() 
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.profession}"