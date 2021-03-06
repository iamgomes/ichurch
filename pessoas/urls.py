from django.urls import path, include
from .views import PessoaList, PessoaPerfil, PessoaUpdate, pessoa_delete, PessoaCreate, pessoa_inativa
from .views import form_cpf, LiderancaList

urlpatterns = [
    path('list/', PessoaList.as_view(), name='pessoa-list'),
    path('new/', PessoaCreate.as_view(), name='pessoa-new'),
    path('delete/<int:pk>', pessoa_delete, name='pessoa-delete'),
    path('perfil/<int:pk>', PessoaPerfil.as_view(), name='pessoa-perfil'),
    path('update/<int:pk>', PessoaUpdate.as_view(), name='pessoa-update'),
    path('search_cpf/', form_cpf, name='search-cpf'),
    path('lideranca_list/', LiderancaList.as_view(), name='lideranca-list'),
    path('inativa/<int:pk>', pessoa_inativa, name='pessoa-inativa'),
]