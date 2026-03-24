
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

        return float(getTimeForAera(tableau,type))
    
def readLengthCSV(type):
    with open(chemin,newline='') as f: #Ouverture du fichier CSV
        tableau=[]
        file=csv.reader(f)
        for ligne in file:
            tableau.append(ligne)

        return float(getTimeForLength(tableau,type))
    

def arrondi_sup_dizaine(v):
    """Arrondi à la dizaine supérieure : 12 -> 20, 20 -> 20, 21 -> 30"""
    return int((v + 9) // 10) * 10

def formater_intervalle(secondes):
    t_min = secondes
    t_max = secondes * 1.2

    if t_max < 60:
        low = arrondi_sup_dizaine(t_min - 10) if t_min > 10 else 0
        high = arrondi_sup_dizaine(t_max)
        return "entre {0} s et {1} s".format(low, high)

    elif t_max < 3600:
        low = int(t_min // 60)
        high = int((t_max + 59) // 60)
        return "entre {0} min et {1} min".format(low, high)

    else:
        low = int(t_min / 360) / 10.0
        high = int(t_max / 360) / 10.0
        return "entre {0} h et {1} h".format(low, high)
