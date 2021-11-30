from django.db import models
from enum import Enum


class TypeChoice(Enum):
    SIMPLE = "simple"
    SPECIALIST = "specialiste"
    MANIPULATION = "manipulation"


class Patient:
    pass


class Doctor:
    pass


class Rdv(models.Model):
    date = models.DateField()
    hours = models.TimeField()
    type = models.CharField(choices=[(tag, tag.value) for tag in TypeChoice])
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(Patient)