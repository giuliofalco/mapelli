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
