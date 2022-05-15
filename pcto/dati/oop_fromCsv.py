#!/usr/bin/python3

# Modulo per l'importazione di dati da csv a database SQLite
# IMPORTAZIONE DA FILE CSV

class Importa:
   # per caricare i dati da un file csv. Classe generica
            
    def __init__(self,nome_file,csep=','):
       self.nome_file = nome_file     # il nome del file da importare
       self.csep = csep               # il carattere separatore
       self.campi = ""                # i nomi dei campi
       self.dati = self.carica_dati() # i dati come lista e l'intestazione con in nomi dei campi
       self.modifica_dati()           # personalizza i dati per adattarli alla particolare tabella

    def modifica_dati(self):
       pass

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

    def json_data(self):
        # trasforma i dati in una stringa json adatta a essere salvata come fixture
        pass
          
class ImportaTutor(Importa):
    # classe specifica per importare i tutor
    
    def __init__(self,nome_file):
        model = "pcto.tutor"
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
           item.append(self.get_email(item[2].lower(),item[1].lower()))
           item.append("Mapelli-2021")

    def togli_id(self):
        # toglie dai dati il primo campo id
        self.dati = [item[1:] for item in self.dati]

class ImportaAziende(Importa):
    # classe specifica per importare le Aziende

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
    # classe specifica per importare le classi da abbinare ai Tutor

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

class ImportaStudenti(Importa):
    # classe specifica per imortare gli studenti

   def modifica_dati(self): 
       self.dati = [item[:3] for item in self.dati]
       for item in self.dati:
        # il primo campo è la classe seguita dall'indirizzo di studi che ignoro
            item[0] = item[0].split()[0]

#### IMPORTAZIONE DATI NEL DATABASE

class DbImport():
  # classe generica per aggiornare il database SQLite

  query="" # query generica da ridefinire nella classi figlie

  def __init__(self,fname,dbname):
       self.dbname = dbname          # nome del database
       self.fname = fname            # nome del file da cui importare

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
   # sottoclasse specifica per popolare il database con i dati dei tutor

    query = "INSERT INTO tutor (cognome,nome,email,password)  VALUES (?,?,?,?)"
    def __init__(self,fname,dbname):
       self.source = ImportaTutor(fname)
       self.dbname = dbname
        
class AziendeImport(DbImport):
     # sottoclasse specifica per popolare il database con i dati delle aziende

    query = "INSERT INTO Aziende (partita_iva,ragione_sociale,sede_comune,sede_provincia,telefono,email,settore) VALUES(?,?,?,?,?,?,?)"
    
    def __init__(self,fname,dbname):
        self.source = ImportaAziende(fname) 
        self.dbname = dbname

class Classi_Tutor(DbImport):
  # per aggiornare i dati delle classi dei tutor. SQLite
   
    query = "update tutor set classi = ? WHERE cognome like ?"

    def __init__(self,fname,dbname):
        self.dbname = dbname
        self.source = ImportaClassi(fname)
      
class StudentiImport(DbImport):
     # sottoclasse specifica per popolare il database con i dati degli studenti

    query = "insert into studenti (classe,cognome,nome) values (?,?,?)"
    def __init__(self,nome_file,dbname,csep=','):
         self.dbname = dbname
         self.csep= csep
         self.source = ImportaStudenti(nome_file,csep)
  





