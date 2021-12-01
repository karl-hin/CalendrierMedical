import time

from django.db import models
from enum import Enum
# for User model extension
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.shortcuts import get_list_or_404


class User(AbstractUser):
    is_patient = models.BooleanField(default=True)


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,
                                related_name='patient_profile')


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,
                                related_name='doctor_profile')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not instance.is_staff:
        if instance.is_patient:
            PatientProfile.objects.get_or_create(user=instance)
        else:
            DoctorProfile.objects.get_or_create(user=instance)
    pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_staff:
        if instance.is_patient:
            instance.patient_profile.save()
        else:
            instance.doctor_profile.save()
    pass


class TypeChoice(Enum):
    SIMPLE = ('SIMPLE', 'simple'),
    SPECIALIST = ('SPECIALIST', 'specialiste'),
    MANIPULATION = ('MANIPULATION', 'manipulation'),


class Rdv(models.Model):
    date = models.DateField()
    hours = models.TimeField()
    type = models.CharField(max_length=30, choices=[(tag, tag.value) for tag in TypeChoice])
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.date + self.hours + self.type

    
# utils functions
def get_available_slots(date):
    rdvs = get_rdv_date(date)
    available_slots = get_daily_slots(date)
    for rdv in rdvs:
        slot_index = available_slots.index(rdv.hours.strftime("%H:%M"))
        if rdv.type == '2':
            del available_slots[slot_index + 3]
            del available_slots[slot_index + 2]
        if rdv.type == '1':
            del available_slots[slot_index + 2]
        del available_slots[slot_index + 1]
        del available_slots[slot_index]
    return available_slots


def get_rdv_date(date):
    return get_list_or_404(Rdv, date=date)


def get_daily_slots(date):
    if date.weekday() <= 3:
        slots = ['08:00', '08:15', '08:30', '08:45', '09:00', '09:15', '09:30', '09:45',
                 '10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30',
                 '14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45',
                 '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30']
    else:
        slots = ['14:00', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30', '15:45',
                 '16:00', '16:15', '16:30']
    # for slot in slots:
    #     slot = time.strptime(slot, '%H:%M')
    return slots
