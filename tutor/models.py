from django.db import models
from django.utils import timezone

class Tipologie_proposte (models.Model):
   # tipologie di proposte
   denominazione = models.CharField(max_length=100)

   def __str__(self):
       return(self.denominazione )

class Tipologie_ente (models.Model):
   # tipologie di proposte
   denominazione = models.CharField(max_length=100)

   def __str__(self):
       return(self.denominazione )

class Indirizzi (models.Model):
   sigla = models.CharField(max_length=100)
   denominazione = models.CharField(max_length=100, blank=True,null=True)

   def __str__(self):
       return(self.denominazione )

class Classi (models.Model):
    classe = models.CharField(max_length=30)
    num_studenti = models.IntegerField(blank=True,null=True)
    indirizzo = models.ForeignKey(Indirizzi, on_delete=models.CASCADE,blank=True,null=True)
    docenti_coinvolti = models.CharField(max_length=200,null=True,blank=True) 

    def __str__(self):
       return(self.classe )
   
    def corso (self):
        # restituisce la sigla del corso
        return self.classe[2:]
    
    class Meta:
        ordering = ['classe']

class Tutor (models.Model):
    cognome = models.CharField(max_length=80)
    nome    = models.CharField(max_length=80,null=True, blank=True)

    def __str__(self):
       return(f"{self.cognome} {self.nome}")
    
    class Meta:
        ordering = ['cognome','nome']

class Studenti(models.Model):

    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    classe = models.ForeignKey(Classi,on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor,null=True,blank=True,on_delete=models.SET_NULL)

    def __str__(self):
       return(self.classe.classe + " - " + self.cognome + " " + self.nome )

    def corso (self):
        # restituisce la sigla del corso
        return self.classe[2:]
    
    class Meta:
        ordering = ['cognome','nome']

class Proposte (models.Model):
    
    nome_progetto = models.CharField(max_length=250)
    disciplina =  models.CharField(max_length=100, null=True, blank=True)
    tipologia = models.ForeignKey(Tipologie_proposte,on_delete=models.CASCADE,null=True, blank=True)
    indirizzo = models.ForeignKey(Indirizzi,on_delete=models.CASCADE,null=True, blank=True)
    max_alunni = models.IntegerField(null=True, blank=True)
    classi_consigliate = models.CharField(max_length=100,null=True,blank=True)
    ente = models.CharField(max_length=100,null=True, blank=True)
    tipo_ente = models.ForeignKey(Tipologie_ente,on_delete=models.CASCADE, null=True, blank=True)
    referente_esterno = models.CharField(max_length=100, null=True, blank=True)
    email_ref_esterno = models.CharField(max_length=50, null=True, blank=True)
    tel_ref_esterno = models.CharField(max_length=50,null=True, blank=True)
    num_ore = models.IntegerField(null=True, blank=True)
    valido_pcto = models.BooleanField (null=True, blank=True)
    data_inizio = models.CharField(max_length=20,null = True, blank=True)
    data_fine = models.CharField(max_length=20,null = True, blank=True)
    descrizione = models.TextField(null=True, blank=True)
    url = models.URLField(null=True,blank=True)
    referenti_interni = models.ManyToManyField(Tutor, blank=True)
    iscrizioni = models.ManyToManyField(Studenti, blank = True)

    def __str__(self):
       return(self.nome_progetto)
    
    class Meta:
        ordering = ['-id']

class News(models.Model):
    autore = models.CharField(max_length=100,blank=True,null=True,default='admin')
    data = models.DateTimeField(blank=True,null=True,default=timezone.now)
    titolo = models.CharField(max_length=100,null=True,blank=True,default='')
    testo = models.TextField()

    def __str__(self):
       return(self.titolo)
    
    class Meta:
        ordering = ['-data']