from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import F, Q, Count, Sum
from .models import Pessoa, FuncaoLideranca
from predios.models import Predio
from .forms import PessoaForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.contrib import messages
import requests
import json
import re
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_text


class PessoaList(LoginRequiredMixin,ListView):
    model = Pessoa
    ordering = ['nome']

    def get_queryset(self):
        queryset = self.model.objects.all()
        nome = self.request.GET.get('nome_contains', None)
        tipo = self.request.GET.get('tipo_exact', None)
        sexo = self.request.GET.get('sexo_exact', None)
        inativo = self.request.GET.get('inativo', None)
        predio = self.request.GET.get('predio_exact', None)

        if nome != '' and nome is not None:
            queryset = queryset.filter(nome__icontains=nome)

        elif sexo != '' and sexo is not None:
            queryset = queryset.filter(sexo=sexo)

        if tipo != '' and tipo is not None:
            queryset = queryset.filter(tipo_pessoa=tipo)

        if inativo == 'on':
            queryset = queryset.filter(ativo=False)

        if predio != '' and predio is not None:
            queryset = queryset.filter(predio=predio)

        return queryset

    def get_context_data(self, **kwargs):
        """ get_context_data let you fill the template context """
        context = super(PessoaList, self).get_context_data(**kwargs)

        context['total_ativos'] = self.get_queryset().filter(ativo=True).count()
        context['total_inativos'] = self.get_queryset().filter(ativo=False).count()

        # calcula a quantidade de pessoas por tipo
        qtde_tipo_pessoa = self.get_queryset().values('tipo_pessoa').annotate(qtdepessoas=Count('id'))
        # aplica o get_display no campo tipo_pessoa
        choices = dict(Pessoa._meta.get_field('tipo_pessoa').flatchoices)
        for entry in qtde_tipo_pessoa:
            entry['tipo_pessoa'] = force_text(choices[entry['tipo_pessoa']], strings_only=True)
        context['qtde_tipo_pessoa'] = qtde_tipo_pessoa

        context['predios'] = Pessoa.objects.values('predio__id','predio__nome').distinct()

        return context

class PessoaPerfil(LoginRequiredMixin,DetailView):
    model = Pessoa

# Não está sendo utilizado. Só está aqui para eu não me esquecer de como faz!!!
class PessoaDelete(SuccessMessageMixin, DeleteView):
    model = Pessoa
    success_url = reverse_lazy('pessoa-list')
    success_message = 'Pessoa "%(nome)s" removida com sucesso.'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(PessoaDelete, self).delete(request, *args, **kwargs)

class PessoaUpdate(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Pessoa
    fields = ['num_cpf','nome','sexo', 'data_nascimento', 'telefone', 'celular', 'email', 'cep', 'rua', 'numero',
    'complemento', 'bairro', 'cidade', 'uf', 'pais', 'tipo_pessoa', 'ativo', 'foto_perfil', 'predio',
    'funcao_lideranca']
    template_name = 'pessoas/pessoa_update_form.html'
    success_url = reverse_lazy('pessoa-list')
    success_message = 'Pessoa "%(nome)s" atualizada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

@login_required
def form_cpf(request):
    return render(request, 'cpf_form.html')

class PessoaCreate(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Pessoa
    fields = '__all__'
    success_url =  reverse_lazy('pessoa-list')
    success_message = 'Pessoa "%(nome)s" adicionada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

    def get_context_data(self, **kwargs):
        context = super(PessoaCreate, self).get_context_data(**kwargs)
        cpf_input = self.request.GET.get('search-cpf') 
        cpf = re.sub('[^0-9]', '', cpf_input)
        if cpf_input is not None:
            r = requests.get('https://api-receita-cpf.herokuapp.com/cpf/{}/?format=json'.format(cpf))
        if r.status_code == 200:
            json = r.json()
        context['result_cpf'] = json
        return context

    def form_valid(self, form):
        f = form.save(commit=False)
        username = f.num_cpf
        firstname = f.nome.split(' ')[0]
        lastname = f.nome.split(' ')[-1]
        senha = make_password('12345senha')
        email = f.email or 'email@email.com'
        f.user = User.objects.create(username=username, first_name=firstname, password=senha,\
            email=email, last_name=lastname)
        f.save()
        return super(PessoaCreate, self).form_valid(form)

@login_required
@csrf_exempt
def pessoa_delete(request, pk):
    User.objects.filter(pessoa=pk).delete() #apaga o usuário da pessoa que autamaticamente apaga a pessoa
    return redirect('pessoa-list')

@login_required
@csrf_exempt
def pessoa_inativa(request, pk):
    Pessoa.objects.filter(pk=pk).update(ativo=False)
    User.objects.filter(pessoa=pk).update(is_active=False)
    return redirect('pessoa-list')

class LiderancaList(LoginRequiredMixin,ListView):
    model = Pessoa
    ordering = ['nome']
    template_name = 'pessoas/lideranca_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(funcao_lideranca__isnull=False)
        nome = self.request.GET.get('nome_contains', None)
        sexo = self.request.GET.get('sexo_exact', None)
        funcao = self.request.GET.get('funcao_exact', None)
        predio = self.request.GET.get('predio_exact', None)
        sem_celula = self.request.GET.get('sem-celula', None)

        if nome != '' and nome is not None:
            queryset = queryset.filter(nome__icontains=nome)

        elif sexo != '' and sexo is not None:
            queryset = queryset.filter(sexo=sexo)

        if funcao != '' and funcao is not None:
            queryset = queryset.filter(funcao_lideranca=funcao)

        if predio != '' and predio is not None:
            queryset = queryset.filter(predio=predio)
        
        #verifica se o campo lider OU discipulador OU supervisor estao nulos
        if sem_celula == 'on':
            queryset = queryset.filter(Líder__isnull=True, Discipulador__isnull=True, Supervisor__isnull=True)

        return queryset

    def get_context_data(self, **kwargs):
        """ get_context_data let you fill the template context """
        context = super(LiderancaList, self).get_context_data(**kwargs)
        context['total_ativos'] = self.get_queryset().filter(ativo=True).count()
        context['total_inativos'] = self.get_queryset().filter(ativo=False).count()
        
        # calcula a quantidade de pessoas por tipo
        qtde_tipo_lideranca = self.get_queryset().\
            values('funcao_lideranca__categoria').annotate(qtdeliderancas=Count('id'))
        # aplica o get_display no campo categoria
        choices = dict(FuncaoLideranca._meta.get_field('categoria').flatchoices)
        for entry in qtde_tipo_lideranca:
            entry['funcao_lideranca__categoria'] = force_text(choices[entry['funcao_lideranca__categoria']], strings_only=True)
        context['qtde_tipo_lideranca'] = qtde_tipo_lideranca

        context['categorias'] = Pessoa.objects.filter(funcao_lideranca__isnull=False).values('funcao_lideranca__id','funcao_lideranca__categoria').distinct()
        context['funcoes'] = Pessoa.objects.filter(funcao_lideranca__isnull=False).values('funcao_lideranca__id','funcao_lideranca__descricao').distinct()
        context['predios'] = Pessoa.objects.filter(funcao_lideranca__isnull=False).values('predio__id','predio__nome').distinct()

        return context