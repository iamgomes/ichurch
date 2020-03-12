from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import F, Q, Count, Sum
from django.utils.encoding import force_text
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Celula
from pessoas.models import Pessoa
from django.views.decorators.csrf import csrf_exempt
import math


class CelulaList(LoginRequiredMixin,ListView):
    model = Celula
    ordering = ['nome']

    def get_context_data(self, **kwargs):
        """ get_context_data let you fill the template context """
        context = super(CelulaList, self).get_context_data(**kwargs)
        context['total_ativos'] = self.model.objects.filter(ativo=True).count()
        context['total_inativos'] = self.model.objects.filter(ativo=False).count()

        # calcula a quantidade de pessoas por tipo
        qtde_tipo_celula = self.model.objects.values('tipo_celula').annotate(qtdecelulas=Count('id'))
        # aplica o get_display no campo tipo_pessoa
        choices = dict(Celula._meta.get_field('tipo_celula').flatchoices)
        for entry in qtde_tipo_celula:
            entry['tipo_celula'] = force_text(choices[entry['tipo_celula']], strings_only=True)
        context['qtde_tipo_celula'] = qtde_tipo_celula

        return context

class CelulaCreate(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Celula
    fields = '__all__'
    success_url =  reverse_lazy('celula-list')
    success_message = 'Célula "%(nome)s" adicionada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

    def get_context_data(self, **kwargs):
        context = super(CelulaCreate, self).get_context_data(**kwargs)
        context['pessoas'] = Pessoa.objects.values('id','nome').order_by('nome')

        return context

    #filtra a lista retornada da ForeignKey dentro do field do form
    def get_form(self, form_class=None):    
        form = super(CelulaCreate, self).get_form(form_class)
        form.fields["lider"].queryset = Pessoa.objects.filter(ativo=True).filter(funcao_lideranca__categoria='L')
        form.fields["discipulador"].queryset = Pessoa.objects.filter(ativo=True).\
            filter(funcao_lideranca__categoria='D')
        form.fields["supervisor"].queryset = Pessoa.objects.filter(ativo=True).\
            filter(Q(funcao_lideranca__categoria='O') | Q(funcao_lideranca__categoria='P'))

        return form

class CelulaUpdate(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Celula
    fields = ['nome', 'tipo_celula', 'dia_semana_reuniao', 'hora_reuniao', 'predio', 'lider', 'discipulador', 
    'supervisor', 'ativo', 'participantes','cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'pais',] 
    success_url = reverse_lazy('celula-list')
    success_message = 'Célula "%(nome)s" atualizada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

        #filtra a lista retornada da ForeignKey dentro do field do form
    def get_form(self, form_class=None):    
        form = super(CelulaUpdate, self).get_form(form_class)
        form.fields["lider"].queryset = Pessoa.objects.filter(ativo=True).filter(funcao_lideranca__categoria='L')
        form.fields["discipulador"].queryset = Pessoa.objects.filter(ativo=True).\
            filter(funcao_lideranca__categoria='D')
        form.fields["supervisor"].queryset = Pessoa.objects.filter(ativo=True).\
            filter(Q(funcao_lideranca__categoria='O') | Q(funcao_lideranca__categoria='P'))

        return form

class CelulaPerfil(LoginRequiredMixin,DetailView):
    model = Celula

@login_required
@csrf_exempt
def celula_delete(request, pk):
    Celula.objects.filter(pk=pk).delete() #apaga o usuário da pessoa que autamaticamente apaga a pessoa
    return redirect('celula-list')

class MinhasCelulasList(LoginRequiredMixin,ListView):
    model = Celula
    ordering = ['nome']
    template_name = 'pequenos_grupos/minhas_celulas.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(\
            Q(lider_id=self.request.user.pessoa.id) | Q(discipulador_id=self.request.user.pessoa.id)\
                | Q(supervisor_id=self.request.user.pessoa.id)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super(MinhasCelulasList, self).get_context_data(**kwargs)
        context['membros'] = self.get_queryset().filter(participantes__tipo_pessoa='M').count()
        context['frequentadores'] = self.get_queryset().filter(participantes__tipo_pessoa='F').count()
        context['visitantes'] = self.get_queryset().filter(participantes__tipo_pessoa='V').count()

        #arredonda o valor para multiplus de 10
        def roundup(x):
            return int(math.ceil(x / 10.0)) * 10

        total_pessoas = context['membros'] + context['frequentadores'] + context['visitantes']

        context['perc_membros'] = roundup((context['membros'] / total_pessoas) * 100)
        context['perc_frequentadores'] = roundup((context['frequentadores'] / total_pessoas) * 100)
        context['perc_visitantes'] = roundup((context['visitantes'] / total_pessoas) * 100)

        return context
