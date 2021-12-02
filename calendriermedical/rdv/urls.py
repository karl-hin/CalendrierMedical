from django.urls import path

from . import views

app_name = 'rdv'
urlpatterns = [
    path('', views.index, name='index'),
    path('addrdvview/<int:doctor>/<int:patient>/<str:date>/<str:type>', views.add_rdv_view, name='add_rdv_view'),
    path('add', views.add, name='add'),
    path('detailsrdv/<int:rdv_id>/', views.details_rdv_view, name='details_rdv_view'),
    path('slots/', views.IndexView.as_view(), name='slots_index'),
    path('getrdvdata/', views.get_rdv_data, name='get_rdv_data'),
]
