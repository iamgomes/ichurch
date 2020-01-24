from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Celula

class CelulaList(LoginRequiredMixin,ListView):
    model = Celula
    ordering = ['nome']

class CelulaCreate(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Celula
    fields = '__all__'
    success_url =  reverse_lazy('celula-list')
    success_message = 'Célula "%(nome)s" adicionada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

class CelulaUpdate(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Celula
    fields = ['nome', 'tipo_celula', 'dia_semana_reuniao', 'hora_reuniao', 'predio', 'lider', 'discipulador', 
    'supervisor', 'situacao', 'cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'uf', 'pais',] 
    template_name = 'pequenos_grupos/celula_form.html'
    success_url = reverse_lazy('celula-list')
    success_message = 'Célula "%(nome)s" atualizada com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)