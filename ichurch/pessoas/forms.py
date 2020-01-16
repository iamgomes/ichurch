from django import forms
from django.db import models
from .models import Pessoa

class PessoaForm(forms.ModelForm):

    class Meta:
        model = Pessoa
        exclude = ('created', 'updated')