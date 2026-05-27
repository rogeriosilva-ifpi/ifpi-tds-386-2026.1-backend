from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Roteador da API
router = DefaultRouter()
router.register(r'selecoes', views.SelecaoModelViewSet)


app_name = 'core'

urlpatterns = [
    path('selecoes/', views.listar_selecoes, name='lista-selecoes'),
    path('sedes/',    views.listar_sedes,    name='lista-sedes'),
    path('',          views.index,           name='index'),
    path('api/', include(router.urls)),
    path('api/sedes', views.SedeCreateListView.as_view()),
    path('api/sedes/<int:id>', views.SedeDetailUpdateDeleteView.as_view())
]
