from django.db import models
from django.template.defaultfilters import date
import datetime
from predios.models import Predio
from django.contrib.auth.models import User
import googlemaps
from django.urls import reverse


class FuncaoLideranca(models.Model):
    CATEGORIA_CHOICES = (
        ('A','Apóstolo'),
        ('D','Discipulador'),
        ('L','Líder'),
        ('P','Pastor'),
        ('O','Obreiro'),
    )

    categoria = models.CharField(max_length=1, choices=CATEGORIA_CHOICES)
    descricao = models.CharField(max_length=100)
    atribuicoes = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = 'Função Liderança'


    def __str__(self):
        return self.descricao


class Pessoa(models.Model):
    SEXO_CHOICES = (
        ('M','Masculino'),
        ('F','Feminino'),
    )

    TIPOPESSOA_CHOICES = (
        ('V','Visitante'),
        ('F','Frequentador'),
        ('M','Membro'),
    )

    SITUACAO_CHOICES = (
        ('A','Ativo'),
        ('I','Inativo'),
    )

    num_cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    data_nascimento = models.DateField(u'Data de Nascimento', auto_now=False, auto_now_add=False)
    telefone = models.CharField(max_length=20, null=True,blank=True)
    celular = models.CharField(max_length=20, null=True,blank=True)
    email = models.EmailField(u'E-mail', null=True,blank=True)
    cep = models.CharField(max_length=9, null=True,blank=True)
    rua = models.CharField(max_length=200, null=True,blank=True)
    numero = models.IntegerField(null=True,blank=True)
    complemento = models.CharField(max_length=200, null=True,blank=True)
    bairro = models.CharField(max_length=50, null=True,blank=True)
    cidade = models.CharField(max_length=50, null=True,blank=True)
    uf = models.CharField(max_length=2, null=True,blank=True)
    pais = models.CharField(max_length=50, null=True,blank=True)
    tipo_pessoa = models.CharField(max_length=1, choices=TIPOPESSOA_CHOICES, default='M')
    situacao = models.CharField(max_length=1, choices=SITUACAO_CHOICES, default='A')
    foto_perfil = models.FileField(upload_to='foto_perfil', blank=True, null=True)
    predio = models.ForeignKey(Predio, on_delete=models.PROTECT, verbose_name='Prédio')
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    funcao_lideranca = models.ForeignKey(FuncaoLideranca, 
            on_delete=models.PROTECT, verbose_name='Função Liderança', blank=True, null=True)
    created = models.DateField(u'Data Cadastro', auto_now=False, auto_now_add=True)
    updated = models.DateField(u'Data Atualização', auto_now=True, auto_now_add=False)

    def get_absolute_url(self):
        return reverse('pessoa-list')
    
    def __str__(self):
        return self.nome

    @property
    def foto_perfil_url(self):
        if self.foto_perfil and hasattr(self.foto_perfil, 'url'):
            return self.foto_perfil.url

    @property
    def matricula(self):
        return '{:0>6}'.format(self.id)

    @property
    def formata_data_nascimento(self):
        return '{}'.format(date(self.data_nascimento, "d/m/Y"))

    @property
    def mes_ano(self):
        return '{}'.format(date(self.created, "Y-m"))

    @property
    def formata_data_cadastro(self):
        return '{}'.format(date(self.created, "d/m/Y"))

    @property
    def idade(self):
        dias = (datetime.date.today() - self.data_nascimento)
        return dias.days // 365

    @property
    def grupo_idade(self):
        if self.idade < 12:
            return u'Criança'
        elif self.idade >= 12 and self.idade < 18:
            return u'Adolescente'
        elif self.idade >= 18 and self.idade < 21:
            return u'Jovem'
        elif self.idade >= 21 and self.idade < 60:
            return u'Adulto'
        elif self.idade >= 60:
            return u'Idoso'

    @property
    def pega_nome_perfil(self):
        nome = self.nome.lower().capitalize().split()
        return nome[0]

    @property
    def geocoding(self):
        address = (str(self.rua) + str(self.numero) + str(self.bairro) + str(self.cidade) + str(self.uf)) or 0
        gmaps = googlemaps.Client(key='AIzaSyDVFn3_PX9ZXlp4Xxm7Fpj6KdBkCruc7YE')
        geocode_result = gmaps.geocode(address)
        return geocode_result[0]['geometry']['location']