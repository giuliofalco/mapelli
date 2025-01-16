from django.db import models

class DayEntry(models.Model):
    date = models.DateField(unique=True)
    assenze = models.TextField(blank=True)   # docenti assenti
    eventi  = models.TextField(blank=True)   # eventi
    uscite  = models.TextField(blank=True)   # Classi in uscita
    note    = models.TextField(blank=True)   # Note varie
    updated_at = models.DateTimeField(auto_now=True)  # Data di ultimo aggiornamento
    
    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
    
    def vuoto(self):
        # restituisce True quando i campi di testo sono tutti vuoti
        return not self.assenze and not self.eventi and not self.uscite and not self.note
