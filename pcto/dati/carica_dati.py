#!/usr/bin/python3
from oop_pcto import *

# AGGIORNAMENTO DATABASE POSTGRES DA SQLITE

# Aggiorno le aziende
#oggetto = AziendePgSQLite('mapelli','pcto.db')
#oggetto.aggiornaDb()

#Aggiorno i Tutor
oggetto = TutorPgSQLite('mapelli','pcto.db')
oggetto.aggiornaDb()

#for item in oggetto.dati:
#    print (item)

print ("Done")
