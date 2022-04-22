#!/usr/bin/python3
from oop_fromDb import *

# AGGIORNAMENTO DATABASE POSTGRES DA SQLITE

# Aggiorno le aziende su Posgres locale
oggetto = AziendePgSQLite('mapelli','pcto.db')
#oggetto.aggiornaDb()

# Aggiorno le aziende su Posgres remoto
#oggetto = Aziende_heroku('mapelli','pcto.db')
#oggetto.aggiornaDb()

#Aggiorno i Tutor
#oggetto = Tutor_heroku('mapelli','pcto.db')
#oggetto.aggiornaDb()

for item in oggetto.dati:
    print (item)

print ("Done")
