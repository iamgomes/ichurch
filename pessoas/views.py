from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import F, Q, Count, Sum
from .models import Pessoa
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

    def get_context_data(self, **kwargs):
        """ get_context_data let you fill the template context """
        context = super(PessoaList, self).get_context_data(**kwargs)
        context['total_ativos'] = Pessoa.objects.filter(situacao='A').count()
        context['total_inativos'] = Pessoa.objects.filter(situacao='I').count()

        # calcula a quantidade de pessoas por tipo
        qtde_tipo_pessoa = Pessoa.objects.values('tipo_pessoa').annotate(qtdepessoas=Count('id'))
        # aplica o get_display no campo tipo_pessoa
        choices = dict(Pessoa._meta.get_field('tipo_pessoa').flatchoices)
        for entry in qtde_tipo_pessoa:
            entry['tipo_pessoa'] = force_text(choices[entry['tipo_pessoa']], strings_only=True)
        context['qtde_tipo_pessoa'] = qtde_tipo_pessoa

        return context

class PessoaPerfil(LoginRequiredMixin,DetailView):
    model = Pessoa

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
    'complemento', 'bairro', 'cidade', 'uf', 'pais', 'tipo_pessoa', 'situacao', 'foto_perfil', 'predio',
    'funcao_lideranca']
    template_name = 'pessoas/pessoa_update_form.html'
    success_url = reverse_lazy('pessoa-list')
    success_message = 'Pessoa "%(nome)s" atualizada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

@login_required
def form_cpf(request):
    return render(request, 'cpf_form.html')

@login_required
def pessoa_create(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            f = form.save(commit=False)
            username = f.num_cpf
            firstname = f.nome.split(' ')[0]
            senha = make_password('12345senha')
            f.user = User.objects.create(username=username, first_name=firstname, password=senha)
            f.save()
            messages.success(request, 'Pessoa "{}" inserida com sucesso!'.format(f.nome))
            return redirect('pessoa-list')
        else:
            print(form.errors)
    else:
        form = PessoaForm()

    cpf_input = request.GET.get('search-cpf') 
    cpf = re.sub('[^0-9]', '', cpf_input)
    if cpf_input is not None:
        r = requests.get('https://api-receita-cpf.herokuapp.com/cpf/{}/?format=json'.format(cpf))
    if r.status_code == 200:
        json = r.json()

    context = {
        'result_cpf': json,
        'form': form
    }
    return render(request, 'pessoas/pessoa_form.html', context)

@login_required
@csrf_exempt
def pessoa_delete(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    pessoa.delete()
    return redirect('pessoa-list')