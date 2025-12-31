from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        # Logic to save User and UserProfile together
        pass 
    return render(request, 'register.html')

def marketplace(request):
    profiles = UserProfile.objects.all()
    return render(request, 'marketplace.html', {'profiles': profiles})