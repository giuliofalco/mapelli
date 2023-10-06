from django.db import models

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
   denominazione = models.CharField(max_length=100)

   def __str__(self):
       return(self.denominazione )

class Classi (models.Model):
   classe = models.CharField(max_length=30)
   num_studenti = models.IntegerField(blank=True,null=True)
   indirizzo = models.ForeignKey(Indirizzi, on_delete=models.CASCADE)

   def __str__(self):
       return(self.classe )

class Studenti(models.Model):

    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    classe = models.ForeignKey(Classi,on_delete=models.CASCADE)

    def __str__(self):
       return(self.classe + " - " + self.cognome + " " + self.nome )

    def corso (self):
        # restituisce la sigla del corso
        return self.classe[2:]

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

    def __str__(self):
       return(self.nome_progetto)
 

