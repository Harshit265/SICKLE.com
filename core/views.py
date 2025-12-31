from django.shortcuts import render, redirect
from .forms import ProfileForm # We will create this next

def select_profession(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('marketplace') # Send them to the interaction hub
    else:
        form = ProfileForm()
    
    return render(request, 'core/select_profession.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the profession selection page immediately!
            return redirect('select_profession') 
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
