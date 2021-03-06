from django.db import models
from predios.models import Predio
from pessoas.models import Pessoa
from django.template.defaultfilters import date
import googlemaps
from django.db.models.signals import post_save
from django.dispatch import receiver


class Celula(models.Model):
    TIPOCELULA_CHOICES = (
        ('A','Adultos'),
        ('J','Jovens'),
        ('C','Crianças'),
        ('M','Mista'),
    )

    DIASEMANA_CHOICES = (
        ('1','Domingo'),
        ('2','Segunda-Feira'),
        ('3','Terça-Feira'),
        ('4','Quarta-Feira'),
        ('5','Quinta-Feira'),
        ('6','Sexta-Feira'),
        ('7','Sábado'),
    )

    nome = models.CharField(max_length=100)
    tipo_celula = models.CharField(max_length=1, choices=TIPOCELULA_CHOICES)
    dia_semana_reuniao = models.CharField(max_length=1, choices=DIASEMANA_CHOICES)
    hora_reuniao = models.TimeField(max_length=6)
    predio = models.ForeignKey(Predio, on_delete=models.PROTECT, verbose_name='Prédio')
    lider = models.ForeignKey(Pessoa, on_delete=models.PROTECT, related_name='Líder')
    discipulador = models.ForeignKey(Pessoa, on_delete=models.PROTECT, related_name='Discipulador')
    supervisor = models.ForeignKey(Pessoa, on_delete=models.PROTECT, related_name='Supervisor')
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
    participantes = models.ManyToManyField(Pessoa)
    ativo = models.BooleanField(default=True, null=False)
    created = models.DateField(u'Data Cadastro', auto_now=False, auto_now_add=True)
    updated = models.DateField(u'Data Atualização', auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.nome

    @property
    def formata_data_cadastro(self):
        return '{}'.format(date(self.created, "d/m/Y"))

    def geocoding(self):
        address = (str(self.rua) + str(self.numero) + str(self.bairro) + str(self.cidade) + str(self.uf)) or 0
        gmaps = googlemaps.Client(key='AIzaSyDVFn3_PX9ZXlp4Xxm7Fpj6KdBkCruc7YE')
        try:
            geocode_result = gmaps.geocode(address)
            codigo = geocode_result[0]['geometry']['location']
        except:
            codigo = ''

        return codigo

@receiver(post_save, sender=Celula)
def update_geocoding(sender, instance, **kwargs):
    codigo = instance.geocoding()
    Celula.objects.filter(id=instance.id).update(lat=codigo['lat'], lng=codigo['lng'])
