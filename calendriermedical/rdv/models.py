from django.db import models
from enum import Enum
# for User model extension
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    if instance.is_patient:
        PatientProfile.objects.get_or_create(user=instance)
    else:
        DoctorProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_patient:
        instance.patient_profile.save()
    else:
        instance.doctor_profile.save()


class TypeChoice(Enum):
    SIMPLE = "simple"
    SPECIALIST = "specialiste"
    MANIPULATION = "manipulation"


class Rdv(models.Model):
    date = models.DateField()
    hours = models.TimeField()
    type = models.CharField(choices=[(tag, tag.value) for tag in TypeChoice])
    doctor = models.ForeignKey(DoctorProfile)
    patient = models.ForeignKey(PatientProfile)