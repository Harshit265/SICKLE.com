from django import forms
from django.core.exceptions import ValidationError
ROLE_CHOICES = [
    ('', '--- Select Role ---'),
    ('farmer', 'Farmer'),
    ('business', 'Business'),
    ('both', 'Both'),
]

class RegistrationForm(forms.Form):
    # ... (name, mobile, email fields here) ...
    user_type = forms.ChoiceField(
        choices=ROLE_CHOICES, 
        widget=forms.Select(attrs={'id': 'role_selector'})
    )
    
    products_offered = forms.CharField(
        label="Which products you have?",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Wheat, Rice, Corn'})
    )
    
    products_needed = forms.CharField(
        label="Which product are you looking for?",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Organic Produce, Bulk Grains'})
    )
    # ... (password fields) ..
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    # This special function checks if the passwords match automatically
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match!")
        return cleaned_data