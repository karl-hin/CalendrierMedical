import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .form import AddRDVForm
from .models import Rdv, DoctorProfile, PatientProfile

from django.views import generic
from .models import *


def index(request):
    rdv_list = Rdv.objects.order_by('-date')

    return render(request, 'rdv/calendar.html', {'rdv_list': rdv_list})


def add(request):
    date_rdv = request.POST['date']
    hours = request.POST['hours']
    type_rdv = request.POST['type']
    patient = PatientProfile.objects.get(pk=request.POST['patient_id'])
    doctor = DoctorProfile.objects.get(pk=request.POST['doctor_id'])
    new_rdv = Rdv(date=date_rdv, hours=hours, type=type_rdv, patient=patient, doctor=doctor)
    new_rdv.save()
    created_rdv = Rdv.objects.latest('id')

    if request.method == 'POST':
        return HttpResponseRedirect('rdv:details_rdv_view', args=(created_rdv.id,))
    else:
        rdv_list = Rdv.objects.order_by('-date')
        return render(request, 'rdv/calendar.html', {'rdv_list': rdv_list})


def details_rdv_view(request, rdv_id):
    rdv = Rdv.objects.get(pk=rdv_id)
    return render(request, 'rdv/detailsrdv.html', {'rdv': rdv})


# def add_rdv_view(request):
#     doctor_list = DoctorProfile.objects.all()
#     patient_list = PatientProfile.objects.all()
#     return render(request, 'rdv/addrdv.html', {'doctor_list': doctor_list,
#                                                'patient_list': patient_list})

def add_rdv_view(request):
    if request.method == 'POST':
        rdv_form = AddRDVForm(request.POST)
        if rdv_form.is_valid():
            # patient = PatientProfile.objects.get(pk=request.POST['patient'])
            # doctor = DoctorProfile.objects.get(pk=request.POST['doctor'])

            return choose_rdv_view(request, rdv_form)
    else:
        rdv_form = AddRDVForm

    return render(request, 'rdv/addrdv.html', {'form': rdv_form})


def choose_rdv_view(request, rdv_form):
    doctor = DoctorProfile.objects.get(pk=rdv_form['doctor'].value())
    p_date = rdv_form['date'].value()
    date = datetime.date(int(p_date.split('-')[0]), int(p_date.split('-')[1]), int(p_date.split('-')[2]))
    slots = get_available_slots(date, doctor.id)

    return render(request, 'rdv/chooserdv.html', {'rdv_form': rdv_form, 'slots': slots})


class IndexView(generic.ListView):
    template_name = 'rdv/index.html'
    context_object_name = 'slots_list'

    def get_queryset(self):
        return get_available_slots(datetime.date.today(), 1)
