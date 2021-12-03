from django import forms

from .models import TypeChoice, DoctorProfile, PatientProfile, TypeChoice2


class AddRDVForm(forms.Form):
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'})
    )
    my_type = forms.ChoiceField(
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


class ChooseRdvForm(forms.Form):
    def __init__(self, my_choice, date, my_type, patient_id, doctor_id, *args, **kwargs):
        super(ChooseRdvForm, self).__init__(*args, **kwargs)
        self.fields['slots'] = forms.ChoiceField(choices=my_choice, widget=forms.RadioSelect())

