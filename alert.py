from datetime import datetime
import sqlite3
import os
import smtplib
import getpass
import sys
from alertconf import *


def mail(type,machine):
    mail = 'univ-avignon'
    user = 'put mail here'
    passwd = 'put password here'
    idMachine = str(machine)

    to = 'put email here'
    subject = 'SYSTEM ALERT !!! '+type
    with open('mail.txt', 'r') as myfile:
        body=myfile.read().replace('\n', '') + idMachine
    try:
        mail = smtplib.SMTP('smtpz.univ-avignon.fr',465)
        mail.ehlo()
        mail.starttls()
        mail.login(user,passwd)
        msg = 'From: ' + user + '\nSubject: ' + subject + '\n' + body
        mail.sendmail(user,to,msg)
        sys.stdout.flush()
        mail.quit()
    except KeyboardInterrupt:
        print ('[-] Annulé')
        sys.exit()
    except smtplib.SMTPAuthenticationError:
        print ('\n[!] Identifiant du compte incorrect!')
        sys.exit()




def main():

    conn = sqlite3.connect("collected_data.db") # connection to db
    c = conn.cursor()   # cursor creation
    c.execute("SELECT memoryPercent,cpuPercent,diskPercent,machineId FROM receivedData ")
    recup=c.fetchall()
    i=0
    while i<len(recup):
        if recup[i][0] > maxRam:
            mail("ALERT RAM",recup[i][3])
        if recup[i][1] > maxCpu:
            mail("ALERT RAM",recup[i][3])
        if recup[i][2] > maxDisk:
            mail("ALERT RAM",recup[i][3])
        i=i+1

main()
