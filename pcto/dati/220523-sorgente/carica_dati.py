#!/usr/bin/python3
from oop_fromDb import *
from oop_fromCsv import *

#### Aggiorno le aziende ####

oggetto = AziendeImport('aziende.csv','pcto.db')
oggetto.aggiornaDb()

#oggetto = AziendePgSQLite('pcto.db','mapelli')
#oggetto.aggiornaDb()

#oggetto = Aziende_heroku('pcto.db','mapelli')
#oggetto.aggiornaDb()

##### Aggiorno i Tutor #####

#oggetto = TutorImport('tutor.csv','pcto.db') # importo i tutor in SQLite
#oggetto.aggiornaDb()

#oggetto = Classi_Tutor('classi_tutor.csv','pcto.db')  # abbino ai tutor le rispettive classi
#oggetto.aggiornaDb()

#oggetto = TutorPgSQLite('pcto.db','mapelli')  # importo tutor e classi in PostgreSQL
#oggetto.aggiornaDb()
                      
#### Aggiorno gli studenti ####

#oggetto = StudentiImport('studenti.csv','pcto.db')
#oggetto.aggiornaDb()

oggetto = StudentiPgSQLite('pcto.db','mapelli')
oggetto.aggiornaDb()
    
#oggetto = Studenti_heroku('mapelli','pcto.db')
#oggetto.aggiornaDb()

#for item in oggetto.dati:
#    print (item)

print ("Done")
