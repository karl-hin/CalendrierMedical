import datetime

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .form import AddRDVForm, ChooseRdvForm
from .models import Rdv, DoctorProfile, PatientProfile

from django.views import generic
from .models import *


def index(request):
    rdv_list = Rdv.objects.order_by('-date')

    return render(request, 'rdv/calendar.html', {'rdv_list': rdv_list})


def add(request):
    date_rdv = request.POST['date']
    hours = request.POST['hours']
    type_rdv = request.POST['my_type']
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
            patient_id = rdv_form['patient'].value()
            doctor_id = rdv_form['doctor'].value()
            date = rdv_form['date'].value()
            my_type = rdv_form['my_type'].value()

            # created_rdv = Rdv.objects.latest('id')
            return HttpResponseRedirect(reverse('rdv:choose_rdv_view',
                                                kwargs={'date': date, 'my_type': my_type, 'patient_id': patient_id,
                                                        'doctor_id': doctor_id}))
    else:
        rdv_form = AddRDVForm

    return render(request, 'rdv/addrdv.html', {'form': rdv_form})


def choose_rdv_view(request, date='', my_type='', patient_id='', doctor_id=''):
    if request.method == 'POST':
        pass
    else:
        s_date = datetime.date(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
        slots = get_available_slots(s_date, doctor_id)
        form = ChooseRdvForm(slots, date, my_type, patient_id, doctor_id)
        print('SLOTS')
        print(slots)
        print(doctor_id)

        return render(request, 'rdv/chooserdv.html', {'form': form, 'date': date, 'my_type': my_type,
                                                      'patient_id': patient_id, 'doctor_id': doctor_id})


class IndexView(generic.ListView):
    template_name = 'rdv/index.html'
    context_object_name = 'slots_list'

    def get_queryset(self):
        return get_available_slots(datetime.date.today(), 1)
