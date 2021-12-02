from django import forms

from .models import TypeChoice, DoctorProfile, PatientProfile, TypeChoice2


class AddRDVForm(forms.Form):
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'})
    )
    type = forms.ChoiceField(
        required=True,
        widget=forms.Select,
        choices=TypeChoice2
    )
    doctor = forms.ModelChoiceField(
        required=True,
        queryset=DoctorProfile.objects.all()
    )
    patient = forms.ModelChoiceField(
        required=True,
        widget=forms.Select,
        queryset=PatientProfile.objects.all()
    )