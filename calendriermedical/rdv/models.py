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
    elif not instance.is_staff:
        DoctorProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_patient:
        instance.patient_profile.save()
    elif not instance.is_staff:
        instance.doctor_profile.save()


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
