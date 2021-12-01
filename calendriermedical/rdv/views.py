import datetime

from django.shortcuts import render

# Create your views here.
from django.views import generic
from .models import *


class IndexView(generic.ListView):
    template_name = 'rdv/index.html'
    # slots_list = get_available_slots(datetime.date.today())
    context_object_name = 'slots_list'

    def get_queryset(self):
        return get_available_slots(datetime.date.today())
