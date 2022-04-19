#!/usr/bin/python3
import sqlite3

class DbImport():
  # classe per aggiornare il database Pg da SQLite
  query = ""         # query di scrittura da ridefinire nella classi figlie
  queryLettura = ""  # query di lettura dei dati
  dati = []          # dati da scrivere con la query

  def __init__(self,target,source):
       self.target = target          # nome del database target
       self.source = source          # nome del database sorgente
       self.leggi()                  # legge i dati come sono
       self.prepara_dati()           # li adatta alle circostanze

  def prepara_dati(self):
      pass

  def leggi(self):
        import sqlite3
        conn = self.connectSQLite() # connessione a sqlite
        cur = conn.cursor()
        cur.execute(self.queryLettura)
        self.dati = cur.fetchall()
       
  def connectSQLite(self):
      import sqlite3
      conn = sqlite3.connect(self.source)
      return conn

  def connectPg(self):
        import psycopg2
        conn = psycopg2.connect(database="mapelli", user="giulio", password="benoni58",host = "127.0.0.1")
        return conn 

  def aggiornaDb(self):              # aggiorna il database utilizzando la query
      conn = self.connectPg()
      cur = conn.cursor()
      cur.executemany(self.query,self.dati)
      conn.commit()

class AziendePgSQLite(DbImport):
    # per aggiornare Pg direttamente da SQLite 
    query = 'INSERT INTO pcto_aziende (partita_iva,ragione_sociale,sede_comune,sede_provincia,telefono,email,settore) VALUES(%s,%s,%s,%s,%s,%s,%s)'
    queryLettura = "SELECT * FROM aziende;"

    def prepara_dati(self):
        self.dati = [item[1:3]+item[4:] for item in self.dati]

class TutorPgSQLite(DbImport):
    queryLettura = "SELECT cognome,nome,email,classi FROM tutor"
    query = "INSERT INTO pcto_tutor (cognome,nome,email,classi) VALUES (%s,%s,%s,%s)"

class Aziende_heroku(AziendePgSQLite):

    def connectPg(self):
        import psycopg2
        conn = psycopg2.connect("dbname=d8tegk8vaiu3ra host=ec2-18-214-134-226.compute-1.amazonaws.com port=5432 user=nmskmnlclwgatl password=c919be0aef8cd19dbe700808ba07d754c6f41a88d20b5ee534df912938f3db63 sslmode=require")
        return conn 

class Tutor_heroku(TutorPgSQLite):
   
    def connectPg(self):
        import psycopg2
        conn = psycopg2.connect("dbname=d8tegk8vaiu3ra host=ec2-18-214-134-226.compute-1.amazonaws.com port=5432 user=nmskmnlclwgatl password=c919be0aef8cd19dbe700808ba07d754c6f41a88d20b5ee534df912938f3db63 sslmode=require")
        return conn 