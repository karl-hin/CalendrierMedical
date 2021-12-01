from django.urls import path

from . import views

app_name = 'rdv'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]