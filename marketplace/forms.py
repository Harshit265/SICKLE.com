from django import forms
from django.core.exceptions import ValidationError

ROLE_CHOICES = [
    ('', '--- Select Role ---'),
    ('farmer', 'Farmer'),
    ('business', 'Business'),
    ('both', 'Both'),
]

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter Full Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@email.com', 'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control'}))
    state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'State / Province', 'class': 'form-control'}))
    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'City / District', 'class': 'form-control'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Full Street Address', 'class': 'form-control', 'rows': 2}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match!")
        return cleaned_data