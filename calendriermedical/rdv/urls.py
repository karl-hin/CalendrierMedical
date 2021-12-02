from django.urls import path

from . import views

app_name = 'rdv'
urlpatterns = [
    path('', views.index, name='index'),
    path('addrdvview', views.add_rdv_view, name='add_rdv_view'),
    path('chooserdvview/', views.choose_rdv_view, name="choose_rdv_view"),
    path('add', views.add, name='add'),
    path('detailsrdv/<int:rdv_id>/', views.details_rdv_view, name='details_rdv_view'),
    path('slots/', views.IndexView.as_view(), name='slots_index')
]
