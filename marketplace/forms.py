from django import forms
from django.core.exceptions import ValidationError
CHOICES = [
    ('', '-- Select Role --'),
    ('business', 'Business'),
    ('farmer', 'Farmer'),
    ('both', 'Both'),
]

class RegistrationForm(forms.Form):
    # ... (previous fields: name, mobile, etc.)
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'id': 'user-type-select'}))
    
    # New Fields
    business_needs = forms.CharField(
        label="What kind of product are you looking for?", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'conditional-field', 'id': 'business-field'})
    )
    farmer_provides = forms.CharField(
        label="What kind of product do you provide?", 
        required=False,
        widget=forms.TextInput(attrs={'class': 'conditional-field', 'id': 'farmer-field'})
    )
    # ... (Keep all your previous fields here) ...
    
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