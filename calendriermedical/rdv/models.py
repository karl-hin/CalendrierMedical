from django.db import models
from enum import Enum
# for User model extension
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Group(Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"


class Profile(models.Models):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(choices=[(tag, tag.value) for tag in Group])

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver()(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
