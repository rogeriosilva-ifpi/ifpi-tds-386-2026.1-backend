from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('selecoes/', views.listar_selecoes, name='lista-selecoes'),
    path('sedes/',    views.listar_sedes,    name='lista-sedes'),
    path('',          views.index,           name='index'),
]
