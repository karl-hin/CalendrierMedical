import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .form import GetRDVForm
# from .models import Rdv, DoctorProfile, PatientProfile

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
        return HttpResponseRedirect(reverse('rdv:details_rdv_view', args=(created_rdv.id,)))
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


def add_rdv_view(request, date='', patient='', type='', doctor=''):
    if request.method == 'POST':
        hours = request.POST['hours']
        doctor_object = DoctorProfile.objects.get(pk=doctor)
        patient_object = PatientProfile.objects.get(pk=patient)
        new_rdv = Rdv(date=date, hours=hours, type=type, patient=patient_object,
                      doctor=doctor_object)
        new_rdv.save()
        created_rdv = Rdv.objects.latest('id')
        return HttpResponseRedirect(reverse('rdv:details_rdv_view', args=(created_rdv.id,)))
    else:
        patient = PatientProfile.objects.get(pk=patient)
        doctor = DoctorProfile.objects.get(pk=doctor)
        return render(request, 'rdv/addrdv.html', {'patient': patient, 'doctor': doctor, 'date':date, 'type': type})


class IndexView(generic.ListView):
    template_name = 'rdv/index.html'
    # slots_list = get_available_slots(datetime.date.today())
    context_object_name = 'slots_list'

    def get_queryset(self):
        return get_available_slots(datetime.date.today(), 1)


def get_rdv_data(request):
    if request.method == 'POST':
        get_rdv_data_form = GetRDVForm(request.POST)
        if get_rdv_data_form.is_valid():
            doctor = get_rdv_data_form['doctor'].value()
            patient = get_rdv_data_form['patient'].value()
            date = get_rdv_data_form['date'].value()
            type = get_rdv_data_form['type'].value()
            return HttpResponseRedirect(reverse('rdv:add_rdv_view', kwargs={'doctor': doctor, 'patient': patient,
                                                                            'date': date, 'type': type, }))
    else:
        get_rdv_data_form = GetRDVForm()

    return render(request, 'rdv/getrdvdata.html', {'form': get_rdv_data_form})
