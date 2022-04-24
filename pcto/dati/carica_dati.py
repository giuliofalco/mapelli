#!/usr/bin/python3
from oop_fromDb import *
from oop_fromCsv import *



                          # IMPORTAZIONE DA FILE CSV

    # Aggiorno i Tutor
#oggetto = ImportaTutor('tutor.csv') 
#oggetto = TutorImport('tutor.csv','pcto.db')
#oggetto.aggiornaDb()
                      

    #Aggiorno gli studenti

#oggetto = ImportaStudenti(nome_file='studenti.csv',csep=';')
#oggetto = StudentiImport(nome_file='studenti.csv',dbname='pcto.db',csep=';')
#oggetto.aggiornaDb()

                    # AGGIORNAMENTO DI DATABASE POSTGRES DA SQLITE

    # Aggiorno le aziende su Posgres locale

#oggetto = AziendePgSQLite('mapelli','pcto.db')
#oggetto.aggiornaDb()

    # Aggiorno gli studenti

#oggetto = StudentiPgSQLite('mapelli','pcto.db')
#oggetto.aggiornaDb()

oggetto = UpdateMailtTutor_heroku('mapelli','pcto.db') # aggiorna le mail di tutor
oggetto.aggiornaDb()

                          # AGGIORNAMENTO DI HEROKU

    # Aggiorno le aziende su Posgres remoto

#oggetto = Aziende_heroku('mapelli','pcto.db')
#oggetto.aggiornaDb()

    # Aggiorno i Tutor

#oggetto = Tutor_heroku('mapelli','pcto.db')
#oggetto.aggiornaDb()

    # Aggiorno gli studenti

#oggetto = Studenti_heroku('mapelli','pcto.db')
#oggetto.aggiornaDb()

#for item in oggetto.dati:
#    print (item)

#for item in oggetto.dati:
#     print (item)

print ("Done")
