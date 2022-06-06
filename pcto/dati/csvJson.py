#!/usr/bin/python

import csv, json

csvFilePath = "tutor.csv"
jsonFilePath = 'tutor.json'

data = []
with open(csvFilePath) as csvFile:
   csvReader = csv.DictReader(csvFile)
   for rows in csvReader:
      data,append(rows)
      
with open(jsonFilePath,'w') as jsonFile:
      jsonFile.write(json.dumps(data, indent=4))
