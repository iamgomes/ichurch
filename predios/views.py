from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import F, Q, Count, Sum
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Predio
from pessoas.models import Pessoa
from pequenos_grupos.models import Celula
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_text


class PredioList(LoginRequiredMixin,ListView):
    model = Predio
    ordering = ['nome']

class PredioPerfil(LoginRequiredMixin,DetailView):
    model = Predio

    def get_context_data(self, **kwargs):
        """ get_context_data let you fill the template context """
        context = super(PredioPerfil, self).get_context_data(**kwargs)
        context['total_pessoas'] = Pessoa.objects.filter(predio_id=self.object.pk).count()
        context['total_celulas'] = Celula.objects.filter(predio_id=self.object.pk).count()
        context['total_lideranças'] = Pessoa.objects.filter(predio_id=self.object.pk).\
            filter(funcao_lideranca__isnull=False).count()

        #extrai dados para gráfico novas pessoas
        #extrai dados para gráfico novas pessoas utilizando property do model
        mes_ano = [p.mes_ano for p in Pessoa.objects.filter(predio_id=self.object.pk)]
        context['totais_mes_ano'] = {x:mes_ano.count(x) for x in set(mes_ano)}

        # calcula a quantidade de pessoas por tipo
        qtde_tipo_pessoa = Pessoa.objects.filter(predio_id=self.object.pk).\
            values('tipo_pessoa').annotate(qtdepessoas=Count('id'))

        # aplica o get_display no campo tipo_pessoa
        choices = dict(Pessoa._meta.get_field('tipo_pessoa').flatchoices)
        for entry in qtde_tipo_pessoa:
            entry['tipo_pessoa'] = force_text(choices[entry['tipo_pessoa']], strings_only=True)
        context['qtde_tipo_pessoa'] = qtde_tipo_pessoa

        #extrai dados para gráfico novas pessoas
        context['predio_pessoas'] = Pessoa.objects.filter(predio_id=self.object.pk).\
            values('predio__nome')\
        .annotate(visitante=Count('id', filter=Q(tipo_pessoa='V')))\
        .annotate(frequentador=Count('id', filter=Q(tipo_pessoa='F')))\
        .annotate(membro=Count('id', filter=Q(tipo_pessoa='M')))
        
        return context

class PredioCreate(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Predio
    fields = '__all__'
    success_url =  reverse_lazy('predio-list')
    success_message = 'Prédio "%(nome)s" adicionado com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

class PredioUpdate(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Predio
    fields = ['num_cnpj','nome','data_abertura', 'telefone', 'email', 'cep', 'rua', 'numero',
    'complemento', 'bairro', 'cidade', 'uf', 'pais', 'tipo_igreja', 'pastor','situacao',] 
    template_name = 'predios/predio_form.html'
    success_url = reverse_lazy('predio-list')
    success_message = 'Prédio "%(nome)s" atualizado com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

@login_required
@csrf_exempt
def predio_delete(request, pk):
    predio = get_object_or_404(Predio, pk=pk)
    predio.delete()
    return redirect('predio-list')