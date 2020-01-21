from django.urls import path, include
from .views import PredioList, PredioCreate, predio_delete

urlpatterns = [
    path('list/', PredioList.as_view(), name='predio-list'),
    path('new/', PredioCreate.as_view(), name='predio-create'),
    path('delete/<int:pk>', predio_delete, name='predio-delete'),
]