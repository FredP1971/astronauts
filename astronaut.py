# librairie HTTP
import requests
# connexion à la BD InfluxDB
# DDL :
#      influx -username admin -password Azertyu1
#      CREATE DATABASE astronauts
#      CREATE USER "astronauts" WITH PASSWORD 'Azertyu1'
#      GRANT ALL ON "astronauts" to "astronauts"
from influxdb import InfluxDBClient

# Astro API returns the current number of people in space.
# When known it also returns the names and spacecraft those people are on.
# URL Website : http://open-notify.org/Open-Notify-API/People-In-Space/
# URL API : http://api.open-notify.org/astros.json
url = "http://api.open-notify.org/astros.json" 
# Appel d'API
url = requests.get(url)
resultat = url.json()
# Nombre d'astronautes
nb = resultat['number']
# Astronautes : mise au format texte
i=0
resultat_formate=''
for astronaut in resultat['people']:
    i=i+1
    resultat_formate=str(resultat_formate) + astronaut['name'] + " - spaceship:" + astronaut['craft'] + " | "

# Structure du résultat à stocker dans la base 'astronauts'
astronauts_data = [
    {
        "measurement" : "Number of astronauts in flight",
        "tags" : {
            "host": "RaspberryPi"
        },
        "fields" : {
            "number": int(nb),
            "astronauts": (resultat_formate)
        }
    }
]
print(astronauts_data)
# Connexion à la base de données InfluxDB, sur la DB 'astronautes'
client = InfluxDBClient('localhost', 8086, 'astronauts', 'Azertyu1', 'astronauts')

#Ecriture de l'enregistrement
client.write_points(astronauts_data)
