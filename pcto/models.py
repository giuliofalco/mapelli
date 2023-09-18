from django.db import models
from django.utils import timezone
from datetime import datetime
from pcto.indirizzi import *

class Tutor(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200,unique=True)
    classi = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
       return(f"{self.cognome} {self.nome}")
    
    class meta:
        ordering = ['cognome','nome']

class Studenti(models.Model):

    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    classe = models.CharField(max_length=200)

    def __str__(self):
       return(self.classe + " - " + self.cognome + " " + self.nome )

    def corso (self):
        # restituisce la sigla del corso
        return self.classe[2:]

class Aziende(models.Model):
    partita_iva = models.CharField(max_length=80,null=True,unique=True)
    ragione_sociale = models.CharField(max_length=200)
    indirizzo = models.CharField(max_length=200,null=True,blank=True)
    comune = models.CharField(max_length=200,null=True)
    provincia = models.CharField(max_length=20,null=True, blank=True)
    cap = models.CharField(max_length=20,null=True,blank=True)
    stato = models.CharField(max_length=20,null=True,blank=True)
    codice_ateco =  models.CharField(max_length=20,null=True,blank=True)
    data_convenzione = models.DateField(null=True,blank=True)
    scadenza_convenzione = models.DateField(null=True,blank=True)
    stagisti = models.ManyToManyField(Studenti,through='Abbinamenti')
    
    def __str__(self):
       return(self.ragione_sociale)
    
    class Meta:
        ordering = ['ragione_sociale']

class Contatti(models.Model):
    data = models.DateField(default=timezone.now)
    azienda = models.ForeignKey(Aziende,to_field='partita_iva',on_delete=models.DO_NOTHING,null=True)
    tutor = models.ForeignKey(Tutor,to_field='email',on_delete=models.CASCADE)
    note = models.TextField(null=True,blank=True)
    responsabile = models.CharField(max_length=100,null=True,blank=True)
    num_studenti = models.IntegerField(default=0)
    periodo_da = models.DateField(null=True,blank=True)
    periodo_a = models.DateField(null=True,blank=True)

    def __str__(self):
       return(self.data.strftime("%d/%m/%Y") + " " + self.tutor.cognome)

    class Meta:
        ordering = ['-data']

    def natural_key(self):
        return (self.data, self.tutor)

class Abbinamenti(models.Model):
   
    studente = models.ForeignKey(Studenti, on_delete=models.CASCADE)
    azienda = models.ForeignKey(Aziende, to_field='partita_iva',on_delete=models.CASCADE)
    periodo_da = models.DateField(null=True,blank=True)
    periodo_a = models.DateField(null=True,blank=True)
   # contatto = models.ForeignKey(Contatti,to_field='data',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
       return(self.studente.cognome)

class Storico(models.Model):
    anno = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    classe = models.CharField(max_length=200)
    indirizzo = models.CharField(max_length=200)
    anno_corso = models.CharField(max_length=200)
    ragione_sociale = models.CharField(max_length=200)
    sede_indirizzo = models.CharField(max_length=200)
    sede_provincia = models.CharField(max_length=200)
    tutor_scuola = models.CharField(max_length=200, null=True,blank=True)
    tutor_azienda = models.CharField(max_length=200, null=True,blank=True)

    def __str__(self):
        return(f"{self.anno} {self.cognome} {self.nome}")