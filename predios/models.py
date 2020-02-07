from django.db import models
from django.template.defaultfilters import date
import datetime
import googlemaps
from django.db.models.signals import post_save
from django.dispatch import receiver


class Predio(models.Model):
    TIPOIGREJA_CHOICES = (
        ('P','PIB Imperial'),
        ('A','Associada'),
    )

    SITUACAO_CHOICES = (
        ('A','Ativo'),
        ('I','Inativo'),
    )

    num_cnpj = models.CharField(max_length=18, blank=True, null=True)
    nome = models.CharField(max_length=100)
    data_abertura = models.DateField(u'Data Abertura',blank=True, null=True, auto_now=False, auto_now_add=False)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(u'E-mail',max_length=100, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)
    rua = models.CharField(max_length=200, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    complemento = models.CharField(max_length=200, null=True,blank=True)
    bairro = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    uf = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=50, null=True,blank=True)
    lat = models.CharField(max_length=20, null=True,blank=True)
    lng = models.CharField(max_length=20, null=True,blank=True)
    tipo_igreja = models.CharField(max_length=1, choices=TIPOIGREJA_CHOICES, default='P')
    situacao = models.CharField(max_length=1, choices=SITUACAO_CHOICES, default='A')
    pastor = models.OneToOneField(to='pessoas.Pessoa', 
            on_delete=models.SET_NULL, related_name='pastor_do_predio', blank=True, null=True)
    created = models.DateField(u'Data Cadastro', auto_now=False, auto_now_add=True)
    updated = models.DateField(u'Data Atualização', auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'Prédios'
    
    @property
    def mes_ano(self):
        return '{}'.format(date(self.created, "Y-m"))
        
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

    def geocoding(self):
        address = (str(self.rua) + str(self.numero) + str(self.bairro) + str(self.cidade) + str(self.uf)) or 0
        gmaps = googlemaps.Client(key='AIzaSyDVFn3_PX9ZXlp4Xxm7Fpj6KdBkCruc7YE')
        geocode_result = gmaps.geocode(address)
        codigo = geocode_result[0]['geometry']['location']
        return codigo

@receiver(post_save, sender=Predio)
def update_geocoding(sender, instance, **kwargs):
    codigo = instance.geocoding()
    Predio.objects.filter(id=instance.id).update(lat=codigo['lat'], lng=codigo['lng'])