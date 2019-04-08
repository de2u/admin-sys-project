import pygal
from datetime import datetime
from random import *
import sqlite3

def affichage_graphe(x):
    line_chart=pygal.Line()
    line_chart.title='Historique de ' + ordi[x]
    line_chart.x_labels = map(str , range(date.hour - 8 , date.hour))
    line_chart.add("Ram", ram[x])
    line_chart.render_to_file('bar_chart.svg')


def affichage(x):
    x=int(x)
    print(ordi[x])
    print('Ordinateur:', ordi[x] ,'\nId:', x ,'\nram:', ram[x][1])
    print('Voulez vous afficher l\'historique de l\'ordinateur ? Y= oui | N= non')
    rep=input()
    if rep == 'Y':
        affichage_graphe(x)
    if rep == 'N':
        welcome()


def welcome():
    conn = sqlite3.connect("collected_data.db")
    cur=conn.cursor()
    global date
    date=datetime.now()
    cur.execute("SELECT machineId FROM receivedData")
    ordi = cur.fetchall()
    print('Bienvenue sur l\'interface de monitoring du parc informatique.')
    print('Il est actuellement ', date.hour,'h',date.minute, '\n')
    print ("Veuillez selectionner la machine que vous desirez obeserver:")
    i=0
    while i<len(ordi):
        print('#',ordi[i][0],'->')
        i=i+1

    print('\nSelection:')
    x=input()
    affichage(x)

def selection():
    welcome()



def main():
    global ordi,id,ram
    ordi = ["pcA", "pcB", "pcC", "pcD","pcE", "pcF","pcG", "pcH","pcI","pcJ"]
    ram = []
    for i in range(10):
        ram.append([])
        for y in range(8):
            ram[i].append( randint(0,16))
    id= [1,2,3,4,5,6,7,8,9,10]
    welcome()


main()
