
import csv
from pathlib import Path

chemin = Path(__file__).parent / "mesureTempsV2.csv"

def getTimeForAera(tab,ligne):
    return tab[ligne][3]

def getTimeForLength(tab,ligne):
    return tab[ligne][2]

def readAreaCSV(type):
    with open(chemin,newline='') as f: #Ouverture du fichier CSV
        tableau=[]
        file=csv.reader(f)
        for ligne in file: 
            tableau.append(ligne) 

        return float(getTimeForAera(tableau,ligne))
    
def readLengthCSV(type):
    with open(chemin,newline='') as f: #Ouverture du fichier CSV
        tableau=[]
        file=csv.reader(f)
        for ligne in file:
            tableau.append(ligne)

        return float(getTimeForLength(tableau,type))

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