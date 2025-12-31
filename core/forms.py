from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profession', 'material_details', 'phone_number']
        widgets = {
            'profession': forms.Select(attrs={'class': 'form-control'}),
            'material_details': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'If farmer, what do you have? If business, what do you want?',
                'rows': 3
            }),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter WhatsApp number (e.g. 919876543210)'}),
        }