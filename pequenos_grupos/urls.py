from django.urls import path, include
from .views import CelulaList, CelulaCreate, CelulaUpdate, CelulaPerfil

urlpatterns = [
    path('list/', CelulaList.as_view(), name='celula-list'),
    path('new/', CelulaCreate.as_view(), name='celula-create'),
    path('update/<int:pk>', CelulaUpdate.as_view(), name='celula-update'),
    path('perfil/<int:pk>', CelulaPerfil.as_view(), name='celula-perfil'),
]