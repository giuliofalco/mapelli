from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from your_app.models import Tutor  # Assicurati di importare il modello Tutor dalla tua app

class Command(BaseCommand):
    help = 'Crea utenti con lo stesso cognome dei tutor'

    def handle(self, *args, **options):
        tutors = Tutor.objects.all()

        for tutor in tutors:
            # Crea un nuovo utente con lo stesso cognome e la password "Mapelli23"
            last_name = tutor.cognome
            username = last_name  # Potresti personalizzare il nome utente in base alle tue esigenze
            password = 'Mapelli23'
            
            # Verifica se esiste già un utente con lo stesso nome utente
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password, last_name=last_name)
                self.stdout.write(self.style.SUCCESS(f'Creato utente con cognome {last_name}: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Utente con nome utente {username} già esistente'))

        self.stdout.write(self.style.SUCCESS('Creazione utenti completata'))
