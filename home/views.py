from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pessoas.models import Pessoa
from predios.models import Predio
from pequenos_grupos.models import Celula
from django.db.models import F, Q, Count, Sum
import json
from django.utils.encoding import force_text
import collections


@login_required
def home(request):
    total_pessoas = Pessoa.objects.count()
    total_predios = Predio.objects.count()
    total_celulas = Celula.objects.count()
    total_liderancas = Pessoa.objects.filter(funcao_lideranca__isnull=False).count()
    
    # calcula a quantidade de pessoas por tipo
    qtde_tipo_pessoa = Pessoa.objects.values('sexo').annotate(qtdepessoas=Count('id'))
    # aplica o get_display no campo tipo_pessoa
    choices = dict(Pessoa._meta.get_field('sexo').flatchoices)
    for entry in qtde_tipo_pessoa:
        entry['sexo'] = force_text(choices[entry['sexo']], strings_only=True)


    #extrai dados para gráfico novas pessoas utilizando property do model mes e ano
    mes_ano = [p.mes_ano for p in Pessoa.objects.all()]
    totais_mes_ano = {x:mes_ano.count(x) for x in set(mes_ano)}

    #extrai dados para gráfico novas pessoas utilizando property do model grupo idade
    grupo_idade = [p.grupo_idade for p in Pessoa.objects.all()]
    totais_grupo_idade = {x:grupo_idade.count(x) for x in set(grupo_idade)}

    #extrai dados para gráfico novas pessoas
    predio_pessoas = Pessoa.objects.values('predio__nome')\
        .annotate(visitante=Count('id', filter=Q(tipo_pessoa='V')))\
        .annotate(frequentador=Count('id', filter=Q(tipo_pessoa='F')))\
        .annotate(membro=Count('id', filter=Q(tipo_pessoa='M')))

    context = {
        'total_pessoas':total_pessoas,
        'total_predios':total_predios,
        'total_celulas':total_celulas,
        'total_liderancas':total_liderancas,
        'qtde_tipo_pessoa':qtde_tipo_pessoa,
        'predio_pessoas':predio_pessoas,
        'totais_mes_ano':totais_mes_ano,
        'totais_grupo_idade':totais_grupo_idade
    }

    return render(request, 'home.html', context)
