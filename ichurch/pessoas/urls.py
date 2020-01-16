from django.urls import path
from .views import PessoaList, PessoaDelete, PessoaPerfil, PessoaUpdate, pessoa_create
from .views import form_cpf

urlpatterns = [
    path('list/', PessoaList.as_view(), name='pessoa-list'),
    path('new/', pessoa_create, name='pessoa-new'),
    path('delete/<int:pk>', PessoaDelete.as_view(), name='pessoa-delete'),
    path('perfil/<int:pk>', PessoaPerfil.as_view(), name='pessoa-perfil'),
    path('update/<int:pk>', PessoaUpdate.as_view(), name='pessoa-update'),
    path('search_cpf/', form_cpf, name='search-cpf'),
]