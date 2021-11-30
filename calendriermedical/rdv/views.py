from datetime import date

from django.shortcuts import render

from calendriermedical.rdv.models import Rdv


def index(request):
    rdv_list = Rdv.objects.order_by('-date')
    doctor_list = Doctor.objects.order_by('-last_name')
    patient_list = Patient.objects.order_by('-last_name')
    return render(request, 'rdv/calendar.html', {'rdv_list': rdv_list, })


def add(request, date, hours, type, patient, doctor):
    new_rdv = Rdv(date=date, hours=hours, type=type, patient=patient, doctor=doctor )
