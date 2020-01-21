from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Pessoa
from .forms import PessoaForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.contrib import messages
import requests
import json
import re
from django.views.decorators.csrf import csrf_exempt


class PessoaList(ListView):
    model = Pessoa
    ordering = ['nome']

class PessoaPerfil(DetailView):
    model = Pessoa

class PessoaDelete(SuccessMessageMixin, DeleteView):
    model = Pessoa
    success_url = reverse_lazy('pessoa-list')
    success_message = 'Pessoa "%(nome)s" removida com sucesso.'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(PessoaDelete, self).delete(request, *args, **kwargs)

class PessoaUpdate(SuccessMessageMixin, UpdateView):
    model = Pessoa
    fields = ['num_cpf','nome','sexo', 'data_nascimento', 'telefone', 'celular', 'email', 'cep', 'rua', 'numero',
    'complemento', 'bairro', 'cidade', 'uf', 'pais', 'tipo_pessoa', 'situacao', 'foto_perfil', 'predio',
    'funcao_lideranca','user']
    template_name = 'pessoas/pessoa_update_form.html'
    success_url = reverse_lazy('pessoa-list')
    success_message = 'Pessoa "%(nome)s" atualizada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)


def form_cpf(request):
    return render(request, 'cpf_form.html')


def pessoa_create(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            f = form.save(commit=False)
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


@csrf_exempt
def pessoa_delete(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    pessoa.delete()
    return redirect('pessoa-list')