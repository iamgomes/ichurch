from django.db import models
from django.template.defaultfilters import date
import datetime


class Predio(models.Model):
    TIPOIGREJA_CHOICES = (
        ('P','PIB Imperial'),
        ('A','Associada'),
    )

    cnpj = models.CharField(max_length=18, blank=True, null=True)
    nome = models.CharField(max_length=100)
    data_abertura = models.DateField(u'Data Abertura',blank=True, null=True, auto_now=False, auto_now_add=False)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(u'E-mail',max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    rua = models.CharField(max_length=200, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    uf = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=50, null=True,blank=True)
    tipo_igreja = models.CharField(max_length=1, choices=TIPOIGREJA_CHOICES, default='P')
    pastor = models.OneToOneField(to='pessoas.Pessoa', 
            on_delete=models.SET_NULL, related_name='pastor_do_predio', blank=True, null=True)
    created = models.DateField(u'Data Cadastro', auto_now=False, auto_now_add=True)
    updated = models.DateField(u'Data Atualização', auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = 'Prédios'

    def __str__(self):
        return self.nome

    @property
    def formata_data_cadastro(self):
        return '{}'.format(date(self.created, "d/m/Y"))

    @property
    def formata_data_multiplicacao(self):
        return '{}'.format(date(self.data_abertura, "d/m/Y"))

    @property
    def idade(self):
        if self.data_abertura:
            dias = (datetime.date.today() - self.data_abertura)
            return dias.days // 365
        else:
            return 'Sem informação'

