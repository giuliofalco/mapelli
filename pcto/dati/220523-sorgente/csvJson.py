#!/usr/bin/python

import csv, json

csvFilePath = "storico.csv"
jsonFilePath = 'storico.json'
model = 'pcto.storico'

data = []
with open(csvFilePath) as csvFile:
   csvReader = csv.DictReader(csvFile,delimiter=';')
   pk = 0
   for rows in csvReader:
      pk = pk + 1
      object = {"model":model,"pk":pk}
      object["fields"] = rows
      data.append(object)
      
with open(jsonFilePath,'w') as jsonFile:
      jsonFile.write(json.dumps(data, indent=4))
