from django.db import models
from django.utils import timezone

LUOGHI = [(0,'Villa Reale'),(1, 'Villasanta'), (2, 'Villa Mirabello')]

class Questionari(models.Model):
    data = models.DateTimeField(default=timezone.now)
    luogo =models.IntegerField(choices=LUOGHI, default='0')
    intervistatore = models.CharField(max_length=100,null=True,blank=True, default="")
    intervistato = models.CharField(max_length=200,null=True,blank=True,default="")

    class Meta:
         ordering = ['luogo','data']
    
    def __str__(self):
        return (f"{LUOGHI[self.luogo]} {self.data}")
    
class Domande(models.Model):
    numero = models.IntegerField(blank=True,null=True)
    testo = models.CharField(max_length=200)

    def __str__(self):
        return (self.testo)
    
    class Meta:
         ordering = ['numero']
    
class Risposte(models.Model):
    domanda = models.ForeignKey(Domande,on_delete=models.CASCADE)
    risposta = models.TextField(null=True,blank=True)
    questionario = models.ForeignKey(Questionari,on_delete=models.CASCADE)
    valutaione = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return (f"{self.questionario.id} {self.domanda} {self.risposta}")
