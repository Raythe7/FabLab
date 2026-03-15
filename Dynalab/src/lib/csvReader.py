
import csv
from pathlib import Path

chemin = Path(__file__).parent / "mesureTemps.csv"

def getMinAire(tab,ligne):
    return tab[ligne][1]

def getMaxAire(tab,ligne):
    return tab[ligne][2]

def getMinLong(tab,ligne):
    return tab[ligne][3]

def getMaxLong(tab,ligne):
    return tab[ligne][4]

def readAreaCSV(type):
    with open(chemin,newline='') as f: #Ouverture du fichier CSV
        tableau=[]
        file=csv.reader(f) #chargement des lignes du fichier csv
        for ligne in file: #Pour chaque ligne...
            #print(ligne, end='\n') #...affichage de la ligne dans la console ...
            tableau.append(ligne) #...on ajoute la ligne dans la liste ...

        return [float(getMinAire(tableau,type)),float(getMaxAire(tableau,type))]
    
def readLengthCSV(type):
    with open(chemin,newline='') as f: #Ouverture du fichier CSV
        tableau=[]
        file=csv.reader(f) #chargement des lignes du fichier csv
        for ligne in file: #Pour chaque ligne...
            #print(ligne, end='\n') #...affichage de la ligne dans la console ...
            tableau.append(ligne) #...on ajoute la ligne dans la liste ...

        return [float(getMinLong(tableau,type)),float(getMaxLong(tableau,type))]

def arrondi(v): 
    if v % 10 < 5:
        return (v//10)*10 #dizaine inf
    else:
        return ((v + 5)//10)*10 #dizaine sup

def transfo(v):
    if v < 60:
        return arrondi(v)
    elif(v >= 60 and v <= 3600):
        return arrondi(v//60)
    else:
        return v//3600
    
def uniteTemps(v):
    if v < 60:
        return "s"
    elif(v >= 60 and v <= 3600):
        return "m"
    else:
        return "h"