#!/usr/bin/python3


class DbImport():
  # classe generale per aggiornare il database Pg da SQLite
  # crere le sottoclassi opportune in funzione del tipo di archivio
  
  import sqlite3
  import psycopg2
  
  query = ""         # query di scrittura da ridefinire nella classi figlie
  queryLettura = ""  # query di lettura dei dati, da ridefinire
  dati = []          # dati da scrivere con la query di aggiornamento del target

  def __init__(self,source,target):
       self.target = target          # nome del database target
       self.source = source          # nome del database sorgente
       self.leggi()                  # legge i dati dal source senza apporre modifiche
       self.prepara_dati()           # li modifica adattandoli alle circostanze

  def prepara_dati(self):
      pass

  def leggi(self):

        conn = self.sqlite3.connect(self.source) # connessione a sqlite della sorgente di dati
        cur = conn.cursor()
        cur.execute(self.queryLettura)
        self.dati = cur.fetchall()
       
  def connectPg(self):
      # si connette al database Postgres locale. Ridefinire in caso di database remoto   
        conn = self.psycopg2.connect(database="mapelli", user="giulio", password="benoni58",host = "127.0.0.1")
        return conn 

  def aggiornaDb(self):              # aggiorna il database target utilizzando la query di scrittura
      conn = self.connectPg()
      cur = conn.cursor()
      cur.executemany(self.query,self.dati)
      conn.commit()

#### Sottoclassi specifiche per aggiornare PosgreSQL locale da SQLite ####

class AziendePgSQLite(DbImport):
    # per aggiornare Aziende su Postgres locale da SQLite 
    query = 'INSERT INTO pcto_aziende (partita_iva,ragione_sociale,tutor_referente_azienda,sede_comune,sede_provincia,telefono,email,settore) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
    queryLettura = "SELECT * FROM aziende;"

class TutorPgSQLite(DbImport):
    # per aggiornare i Tutor
    queryLettura = "SELECT cognome,nome,email,classi FROM tutor"
    query = "INSERT INTO pcto_tutor (cognome,nome,email,classi) VALUES (%s,%s,%s,%s)"

class StudentiPgSQLite(DbImport):
    # per aggiornare gli studenti
     queryLettura = "SELECT cognome,nome,classe FROM studenti"
     query = "INSERT INTO pcto_studenti (cognome,nome,classe) VALUES (%s,%s,%s)"

class UpdateMailTutor(DbImport):
    # aggiorna solo le email sui Tutor 

    query = "update pcto_tutor set email = %s where nome = %s and cognome = %s"
    queryLettura = "select email, nome, cognome from tutor"

###############  Classi per aggiornare Heroku ###############

class HerokuDb():
    # classe generale con il metodo e le credenziali per il collegamento a Heroku

    def connectPg(self):
        import psycopg2
        conn = psycopg2.connect("dbname=d8tegk8vaiu3ra host=ec2-18-214-134-226.compute-1.amazonaws.com port=5432 user=nmskmnlclwgatl password=c919be0aef8cd19dbe700808ba07d754c6f41a88d20b5ee534df912938f3db63 sslmode=require")
        return conn 

class Aziende_heroku(AziendePgSQLite,HerokuDb):
    # Aggiorna Aziende su Heroku
    def __init__(self):
        connectPg = HerokuDb.connectPg

class Tutor_heroku(TutorPgSQLite,HerokuDb):
    # Aggiorna Tutor su Heroku

    def __init__(self):
        connectPg = HerokuDb.connectPg
   
class Studenti_heroku(StudentiPgSQLite,HerokuDb):
    # Aggiorna Sudenti su Heroku

    def __init__(self):
        connectPg = HerokuDb.connectPg

class UpdateMailtTutor_heroku(UpdateMailTutor,HerokuDb):
    # Aggiorna solo le email su Heroku

    def __init__(self):
        connectPg = HerokuDb.connectPg