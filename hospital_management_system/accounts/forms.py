from django import forms

class RegistrationForm(forms.Form):
    ROLE_CHOICES = [
        ("doctor", "Doctor"),
        ("patient", "Patient"),
        ("receptionist", "Receptionist")  # Added Receptionist role
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select())
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(max_length=100)
    
    # Doctor-specific fields
    qualification = forms.CharField(max_length=200, required=False)
    experience = forms.IntegerField(required=False)
    specialization = forms.CharField(max_length=100, required=False)
    
    # Patient-specific fields
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female")], required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    contact = forms.CharField(max_length=15, required=False)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)
    
    # Receptionist-specific fields
    contact_receptionist = forms.CharField(max_length=15, required=False)  # Contact for receptionist


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
