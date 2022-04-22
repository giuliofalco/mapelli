from django.db import models
from django.utils import timezone
from datetime import datetime

class Tutor(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    classi = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
       return(f"{self.cognome} {self.nome}")
    
    class meta:
        ordering = ['cognome','nome']

class Aziende(models.Model):
    partita_iva = models.CharField(max_length=80,null=True,unique=True)
    ragione_sociale = models.CharField(max_length=200)
    tutor_referente_azienda = models.CharField(max_length=200,null=True,blank=True)
    sede_comune = models.CharField(max_length=200,null=True)
    sede_provincia = models.CharField(max_length=20,null=True)
    telefono = models.CharField(max_length=200,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    settore = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
       return(self.ragione_sociale)
    
    class Meta:
        ordering = ['ragione_sociale']

class Contatti(models.Model):
    data = models.DateField(default=timezone.now)
    azienda = models.ForeignKey(Aziende,to_field='partita_iva',on_delete=models.DO_NOTHING,null=True)
    tutor = models.ForeignKey(Tutor,on_delete=models.CASCADE)
    note = models.TextField(null=True,blank=True)
    responsabile = models.CharField(max_length=100,null=True,blank=True)
    num_studenti = models.IntegerField(default=0)
    periodo_da = models.DateField(null=True,blank=True)
    periodo_a = models.DateField(null=True,blank=True)

    def __str__(self):
       return(self.data.strftime("%d/%m/%Y"))

    class Meta:
        ordering = ['-data']