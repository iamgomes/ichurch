from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Predio
from django.views.decorators.csrf import csrf_exempt


class PredioList(ListView):
    model = Predio
    ordering = ['nome']

class PredioCreate(SuccessMessageMixin, CreateView):
    model = Predio
    fields = '__all__'
    success_url =  reverse_lazy('predio-list')
    success_message = 'Prédio "%(nome)s" adicionado com sucesso.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, nome=self.object.nome)

@csrf_exempt
def predio_delete(request, pk):
    predio = get_object_or_404(Predio, pk=pk)
    predio.delete()
    return redirect('predio-list')