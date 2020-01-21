from django.contrib import admin
from .models import Pessoa, FuncaoLideranca

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('num_cpf','nome','email','celular','tipo_pessoa','situacao')

admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(FuncaoLideranca)
