from django.urls import path, include
from .views import PessoaList, PessoaPerfil, PessoaUpdate, pessoa_delete, PessoaCreate
from .views import form_cpf, LiderancaList

urlpatterns = [
    path('list/', PessoaList.as_view(), name='pessoa-list'),
    path('new/', PessoaCreate.as_view(), name='pessoa-new'),
    path('delete/<int:pk>', pessoa_delete, name='pessoa-delete'),
    path('perfil/<int:pk>', PessoaPerfil.as_view(), name='pessoa-perfil'),
    path('update/<int:pk>', PessoaUpdate.as_view(), name='pessoa-update'),
    path('search_cpf/', form_cpf, name='search-cpf'),
    path('lideranca-list/', LiderancaList.as_view(), name='lideranca-list'),
]