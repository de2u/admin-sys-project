import pygal
from datetime import datetime
import sqlite3

def affichage_graphe(id,ram,cpu,disk):                                  #crée un fichier SVG de l'historique des perfs de la machine selectionné
    line_chart=pygal.Line(range=(0,100))                                #creation graphe linaire avec une range sur l'axe Y de 0 à 100
    line_chart.title='Historique de '
    line_chart.x_labels = map(str , range(date.hour - 8 , date.hour))
    line_chart.add("Ram", ram)                                          #ajout ligne de donnée de la ram
    line_chart.add("CPU", cpu)                                          #ajout ligne de donnée du cpu
    line_chart.add("Disk", disk)                                        #ajout ligne de donnée du disk
    line_chart.render_to_file('bar_chart.svg')                          #rendu du graphe en fichier svg




def affichage(x):                                                       #recupere les perf de l'ordinateur selectionné depuis la bdd
    conn = sqlite3.connect("collected_data.db") # connection to db
    c = conn.cursor()   # cursor creation
    xVal=(x,)

    c.execute("SELECT memoryPercent,cpuPercent,diskPercent FROM receivedData WHERE machineId = ? ORDER BY datestamp DESC" , xVal) #selection de critere memoir, cpu et disk de la machine selectionné dans l'ordre du plus recent au plus vieux
    recup=c.fetchall()
    print(recup)
    ram=[]
    cpu=[]
    disk=[]
    i=0
    while i<len(recup):             #stockage des données recuperé depuis la bdd dans des tableaux
        ram.append(recup[i][0])
        cpu.append(recup[i][1])
        disk.append(recup[i][2])
        i=i+1

    print('Ordinateur:\nId:', x ,'\nram:', ram[0],'\ncpu:', cpu[0],'\ndisk:', disk[0])  #affiche les dernieres infos recupéré par la sonde pour l'ordinateur selectionné
    print('Voulez vous afficher l\'historique de l\'ordinateur ? Y= oui | N= non')

    rep=input()
    while rep != 'Y'||rep!='N':      #Si 
        if rep == 'Y':
            conn.close()
            affichage_graphe(x,ram,cpu)         #appel de la fonction pour creer le graphe
        if rep == 'N':
            conn.close()
            welcome()



def welcome():
    conn = sqlite3.connect("collected_data.db")
    cur=conn.cursor()
    global date, ordi
    date=datetime.now()
    cur.execute("SELECT DISTINCT machineId FROM receivedData")
    ordi = cur.fetchall()
    print('Bienvenue sur l\'interface de monitoring du parc informatique.')
    print('Il est actuellement ', date.hour,'h',date.minute, '\n')
    print ("Veuillez selectionner la machine que vous desirez obeserver:")
    i=0
    while i<len(ordi):
        print('#',i, "->", ordi[i][0])
        i=i+1

    print('\nSelection:')
    x=input()
    x=int(x)
    conn.close()

    affichage(ordi[x][0])


def main():
    welcome()


main()
