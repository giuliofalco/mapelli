from mapelli.models import Tutor
import csv

def run():
    with open('mapelli/tutor.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Tutor.objects.all().delete()

        for row in reader:
            print(row)

            tutor = Tutor(cognome=row[0],
                        nome=row[1],
                        classi=row[2])
            tutor.save()