def oeffnen(Datei,Modus):
    # Modul zum öffnen der Datei
    try:
        d = open(Datei, Modus)
    except:
        print("Datei nicht gefunden")
        sys.exit(0)
    return (d)

# Start
#import sys, urllib,requests
#import time

def eingabe():
    # Modul zur Eingabe der Messparameter
    # Wie lange und mit welchem Intervall soll die Messung laufen
    print ("Messdauer in Stunden eingeben:", end= " ")
    Dauer = input()
    Dauer = float(Dauer)
    Dauer = int(Dauer)
    print ( "Messintervall in Minuten eingeben:", end= " ")
    Intervall = input()
    Intervall = float(Intervall)
    Intervall = int(Intervall)
    Dauer_sec = Dauer * 3600
    print (Dauer_sec)
    Intervall_sec = Intervall * 60
    print(Intervall_sec)
    return Dauer_sec, Intervall_sec

# Start der Messung und Auswertung
import sys, urllib,requests
import time

# Einlesen
(Ds,Is) = eingabe ()

# Datum bestimmen
Datum = time.strftime("%a, %d %b %Y")

# Datum und Kopf zum Start ind csv-Datei schreiben
d = oeffnen("Messdaten.csv","w")
d.write (Datum + ";" + "Temperatur" + ";" + "rel.Feuchte" + "\n")
d.close()

# Wie lange soll die Messung laufen
end_time=time.time() + Ds

# So lange soll die Messung laufen
while time.time() < end_time:
    # Verbindung zum Sensor...
    try:
        u = urllib.request.urlopen ("http://sensor1:8080")
    except:
        print("Fehler")
        sys.exit(0)
    # ... und in eine Liste einlesen
    li = u.readlines()
    # ... und wieder schließen
    u.close()

    # Ausgabe der Werte
    for Wert in li:
        #Poistion von Temp- und Feuchtewerte finden
        Wert_str = str(Wert).replace(".",",")
        Pos1 = Wert_str.find("temp")
        #print (Pos1)
        Pos2 = Wert_str.find("rel")
        #print (Pos2)
        Zeit = (time.strftime("%H:%M:%S"))
        Temp = Wert_str[Pos1+6:Pos1+11]
        Feuchte = Wert_str[Pos2+5:Pos2+8]
        # und Ausgabe am Bilschirm
        print ("Zeit: ",Zeit,"Temperatur: ",Temp,"°C","Luftfeuchte:", Feuchte, "% rel.")
        # und Ausgabe als CSV-Datei
        # Zugriff auf Ausgabe-Datei
        d = oeffnen("Messdaten.csv", "a")
        # schreiben in Datei als csv
        d.write(Zeit + ";" + Temp + ";"+ Feuchte+ "\n")
        # und schließen
        d.close()
        # Intervall abwarten
        time.sleep(Is)

