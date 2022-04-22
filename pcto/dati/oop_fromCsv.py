#!/usr/bin/python3
import sqlite3

class Importa:
   # per caricare i dati da un file csv
            
   def __init__(self,nome_file,csep=','):
       self.nome_file = nome_file     # il nome del file da importare
       self.csep = csep               # il carattere separatore
       self.campi = ""                # i nomi dei campi
       self.dati = self.carica_dati() # i dati come lista e l'intestazione con in nomi dei campi
       
   def get_email(self,nome,cognome):
       #restituisce la mail istituzionale del Mapelli, dati nome e cognome
       return(nome.lower() + "." + cognome.lower() + "@mapelli-monza.edu.it")
       
   def carica_dati(self):
      #  carica il file di dati, utilizza la prima riga per inizializzare l'intestazione
      #  prepara la lista dati ottenuta separando i campi, togliendo il fine stringa ed eliminando    
      #  l'intestazione
      
      f = open(self.nome_file,"r")
      listaRighe = f.readlines()    # legge tutte le righe del file e restituisce la lista delle righe
      f.close()                     # chiudo il file
      testa = listaRighe[0].strip() # memorizza in testa, la prima riga
      self.campi = testa.strip().split(self.csep)   # inizializza self.campi con la lista dei campi
      listaRighe = listaRighe[1:]   # toglie la prima riga da listaRighe
      return [item.strip().split(self.csep) for item in listaRighe] 
                                    # ritorna la lista con campi separati
          
class ImportaTutor(Importa):
    
    def __init__(self,nome_file):
        super().__init__(nome_file)
        self.lower_nomi()
        self.fill_data()
        self.togli_id()

    def lower_nomi(self):
        # sistema i cognomi e i nomi con la prima lettera maiuscola e il resto minuscolo
        for i in range(len(self.dati)):
           self.dati[i][1] = self.dati[i][1].capitalize()
           self.dati[i][2] = self.dati[i][2].capitalize() 

    def fill_data(self): 
        # fill data with email and password
        for item in self.dati:
           item.append(self.get_email(item[1].lower(),item[0].lower()))
           item.append("Mapelli-2021")

    def togli_id(self):
        # toglie dai dati il primo campo id
        self.dati = [item[1:] for item in self.dati]

class ImportaAziende(Importa):
    # importa direttamente da file tsv originale con tutti i campi
    def __init__(self,fname):
        super().__init__(fname,';')    
        self.dati = [[item[2],item[0],item[4],item[6],item[8],item[9],item[16]] for item in self.dati]
        self.elimina_duplicati()

    def elimina_duplicati(self):
        # toglie le linee duplicate presenti in dati
        piva = set()
        new_list = []
        for item in self.dati:
            if not item[0] in piva:
               new_list.append(item)
               piva.add(item[0])
        self.dati = new_list
    

class ImportaClassi(Importa):
    def __init__(self,fname):
        super().__init__(fname) 
        self.dati = self.raccogli_classi()
        self.dati = self.inverti()

    def raccogli_classi(self):
       # raccoglie i dati per aggiornare il db
       diz = {}   # dizionario con chiave il tutor e valore la stringa con la classi
       for riga in self.dati:
           for item in riga[2:]:
               if item:
                  diz[item] = diz.get(item,'') + riga[0] + ' '
       return diz.items()

    def inverti(self):
       return [(item[1],item[0]) for item in self.dati]

class DbImport():
  # classe per aggiornare il database
  query="" # query generica da ridefinire nella classi figlie

  def __init__(self,fname,dbname):
       self.dbname = dbname          # nome del database

  def connect(self):
      import sqlite3
      conn = sqlite3.connect(self.dbname)
      return conn
  
  def aggiornaDb(self):              # aggiorna il database utilizzando la query
      conn = self.connect()
      cur = conn.cursor()
      cur.executemany(self.query,self.source.dati)
      conn.commit()
      
class TutorImport(DbImport):
   # sottoclasse che specifica la query da utilizzare
   query = "INSERT INTO tutor (cognome,nome,email,password)  VALUES (?,?,?,?)"
   def __init__(self,fname,dbname):
       self.source = ImportaTutor(fname)
       self.dbname = dbname

class TutorImportPg(TutorImport):
   # per connettersi al database su PostgreSQL tabella "OffPcto_tutor" di mysite usando con Django
   
    query = 'INSERT INTO "OffPcto_tutor" (cognome,nome,email) VALUES (%s,%s,%s)'

    def __init__(self,fname,dbname):
        super().__init__(fname,dbname)
        for item in self.source.dati:
            item.pop()                # tolgo la password dai dati

    def connect(self):
        import psycopg2
        conn = psycopg2.connect(database="mysite", user="giulio", password="benoni58",host = "127.0.0.1")
        return conn    

class TutorImportHeroku(TutorImportPg):

    def connect(self): 
        import psycopg2  
        conn =  psycopg2.connect("dbname=d3034gq117jmk1 host=ec2-44-194-167-63.compute-1.amazonaws.com port=5432 user=yycpzjmtozwhci password=4b99951991961c1f66cd7f0f07dbe35972aa854164f9f7fc31b37237c3bc8827 sslmode=require")
        return conn  
         
class AziendeImport(DbImport):
    query = "INSERT INTO Aziende (partita_iva,ragione_sociale,sede_comune,sede_provincia,telefono,email,settore) VALUES(?,?,?,?,?,?,?)"
    
    def __init__(self,fname,dbname):
        self.source = ImportaAziende(fname) 
       
class AziendeImportPg(AziendeImport):
   
    query = 'INSERT INTO "OffPcto_aziende" (partita_iva,ragione_sociale,sede_comune,sede_provincia,telefono,email,settore) VALUES(%s,%s,%s,%s,%s,%s,%s)'
   
    def connect(self):
      import psycopg2
      conn = psycopg2.connect(database="mysite", user="giulio", password="benoni58",host = "127.0.0.1")
      return conn

class AziendeImportHeroku(AziendeImportPg):

    def connect(self):
      import psycopg2
      conn =  psycopg2.connect("dbname=d3034gq117jmk1 host=ec2-44-194-167-63.compute-1.amazonaws.com port=5432 user=yycpzjmtozwhci password=4b99951991961c1f66cd7f0f07dbe35972aa854164f9f7fc31b37237c3bc8827 sslmode=require")
      return conn

class Classi_tutor(DbImport):
  # per aggiornare i dati delle classi dei tutor. SQLite
   
    query = "update tutor set classi = ? WHERE cognome like ?"

    def __init__(self,fname,dbname):
        self.dbname = dbname
        self.source = ImportaClassi(fname)
      
class Classi_tutorPg(Classi_tutor):
  # per connettersi al Postgres locale Django OffPcto
     
    query = 'update "OffPcto_tutor" set classi = %s WHERE cognome like %s'

    def connect(self): 
        import psycopg2  
        conn = psycopg2.connect(database="mysite", user="giulio", password="benoni58",host = "127.0.0.1")
        return conn  
  
class Classi_tutorHeroku(Classi_tutorPg):
  # per connettersi al Postgres di Heroku
     
    def connect(self): 
        import psycopg2  
        conn =  psycopg2.connect("dbname=d3034gq117jmk1 host=ec2-44-194-167-63.compute-1.amazonaws.com port=5432 user=yycpzjmtozwhci password=4b99951991961c1f66cd7f0f07dbe35972aa854164f9f7fc31b37237c3bc8827 sslmode=require")
        return conn

class AziendePgSQLite(AziendeImportPg):
    # per aggiornare Pg direttamente da SQLite 
    
    queryLettura = "SELECT * FROM aziende;"

    def __init__(self,pgname,sqlite):
        self.dbname = pgname # il database su cui scrivere
        self.sqlite = sqlite # il database da cui leggere
        self.leggi()

    def leggi(self):
        import sqlite3
        connSqlite = sqlite3.connect(self.sqlite) # connessione a sqlite
        cur = connSqlite.cursor()
        cur.execute(self.queryLettura)
        self.dati = cur.fetchall()
        self.dati = [item[1:3]+item[4:] for item in self.dati]

    def aggiornaDb(self):
        conn = self.connect()  # si connette al postgres
        cur = conn.cursor()
        cur.executemany(self.query,self.dati)
        conn.commit()


