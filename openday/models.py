from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class News(models.Model):
    autore = models.CharField(max_length=100,blank=True,null=True,default='admin')
    data = models.DateTimeField(blank=True,null=True,default=timezone.now)
    titolo = models.CharField(max_length=100,null=True,blank=True,default='')
    testo = RichTextField()

    def __str__(self):
       return(self.titolo)
    
    class Meta:
        ordering = ['-data']

class Eventi(models.Model):
    data = models.CharField(max_length=80,blank=True,null=True)
    sigla = models.CharField(max_length=30)
    titolo =  models.CharField(max_length=100, blank=True, null=True)
    descrizione = RichTextField(blank=True, null=True, default='')
    luogo = models.CharField(max_length=100, blank=True, null=True, default='scuola')
    indirizzo = models.CharField(max_length=100, blank=True, null=True)
    referente =  models.CharField(max_length=100, blank=True, null=True)
    telefono =  models.CharField(max_length=50, blank=True, null=True) 
    email = models.EmailField(blank=True,null=True)
    attivo = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.titolo} {self.data}"
   
RUOLO = [(0,'genitore'),(1,'studente'),(2,'docente')]
class Visitatori(models.Model):
    cognome =  models.CharField(max_length=100)
    nome = models.CharField(max_length=100,default='')
    email = models.EmailField(blank=True,null=True)
    comune =  models.CharField(max_length=80, blank=True, null=True)
    scuola =  models.CharField(max_length=80, blank=True, null=True)
    ruolo = models.IntegerField(choices=RUOLO, blank=True, null=True,default=0)

    def __str__(self) -> str:
        return f"{self.cognome} {self.nome}"

class Iscrizioni(models.Model):
    visitatore = models.ForeignKey(Visitatori,on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventi, on_delete=models.CASCADE)
    data_iscrizione = models.DateTimeField(default=timezone.now) 
    presente = models.BooleanField(default=False,blank=True)

class Indirizzi(models.Model):
    titolo = models.CharField(max_length=50)
    banner = models.ImageField(null=True,blank=True)
    descrizione = RichTextField()

    def __str__(self) -> str:
        return self.titolo
    
class riga_orario(models.Model):
    materia = models.CharField(max_length=80)
    prima   = models.IntegerField(null=True,blank=True)
    seconda = models.IntegerField(null=True,blank=True)
    terza   = models.IntegerField(null=True,blank=True)
    quarta  = models.IntegerField(null=True,blank=True)
    quinta  = models.IntegerField(null=True,blank=True)
    indirizzo = models.ForeignKey(Indirizzi,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f" {self.indirizzo} {self.materia}"