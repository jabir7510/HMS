from django import forms

class UpdatePatientForm(forms.Form):
    name = forms.CharField(max_length=255)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    address = forms.CharField(widget=forms.Textarea)
    contact = forms.CharField(max_length=20)
    medical_history = forms.CharField(widget=forms.Textarea)
