import pygal
from datetime import datetime
import sqlite3

def affichage_graphe(id,ram,cpu,disk):
    line_chart=pygal.Line(range=(0,100))
    line_chart.title='Historique de '
    line_chart.x_labels = map(str , range(date.hour - 8 , date.hour))
    line_chart.add("Ram", ram)
    line_chart.add("CPU", cpu)
    line_chart.add("Disk", disk)
    line_chart.render_to_file('bar_chart.svg')




def affichage(x):
    conn = sqlite3.connect("collected_data.db") # connection to db
    c = conn.cursor()   # cursor creation
    xVal=(x,)

    c.execute("SELECT memoryPercent,cpuPercent,diskPercent FROM receivedData WHERE machineId = ? ORDER BY datestamp ASC" , xVal)
    recup=c.fetchall()
    print(recup)
    ram=[]
    cpu=[]
    disk=[]
    i=0
    while i<len(recup):
        ram.append(recup[i][0])
        cpu.append(recup[i][1])
        disk.append(recup[i][2])
        i=i+1

    print(ram)
    print('Ordinateur:\nId:', x ,'\nram:', ram[0])
    print('Voulez vous afficher l\'historique de l\'ordinateur ? Y= oui | N= non')

    rep=input()
    if rep == 'Y':

        conn.close()
        affichage_graphe(x,ram,cpu)
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
    print("\033[1;32;40m Bright Green  \n\033[0;37;40m")
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

def selection():
    welcome()



def main():
    welcome()


main()
