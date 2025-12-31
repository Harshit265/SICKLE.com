from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .forms import ProfileForm

# Matches path('', views.home)
def home(request):
    return render(request, 'core/home.html')

# Matches path('register/', views.register_view)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('select_profession')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

# Matches path('profession/', views.select_profession)
def select_profession(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('marketplace')
    else:
        form = ProfileForm()
    return render(request, 'core/select_profession.html', {'form': form})

# Matches path('marketplace/', views.marketplace)
def marketplace(request):
    all_profiles = Profile.objects.all()
    return render(request, 'core/marketplace.html', {'all_profiles': all_profiles})
def home(request):
    # This must match the folder structure: templates/core/home.html
    return render(request, 'core/home.html')
from django.shortcuts import redirect

def register_view(request):
    # ... after your form saves and user logs in ...
    return redirect('select_profession') # Sends user to the next page
def select_profession(request):
    # This is the "second page" where users choose Farmer/Business
    return render(request, 'core/select_profession.html')

def marketplace(request):
    # This is where interaction happens via WhatsApp/Phone
    return render(request, 'core/marketplace.html')