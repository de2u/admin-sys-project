import sqlite3
import time
import datetime
import os
from os import walk

db_name = 'collected_data.db'
conn = sqlite3.connect(db_name) # connection to db
c = conn.cursor()   # cursor creation

def create_receivedData_table():
    # table creation if inexistent
    c.execute('CREATE TABLE IF NOT EXISTS receivedData(unix_rec INTEGER, unix_insert INTEGER, datestamp TEXT, machineId INTEGER PRIMARY KEY, cpuPercent REAL, memoryPercent REAL, diskPercent REAL)')

# def create_machineInfo_table():
#     c.execute('CREATE TABLE IF NOT EXISTS machineInfo(machineId REAL, OS TEXT)')

def read_receivedData():
    print(50*'#')
    c.execute('SELECT * FROM receivedData')
    [print(row) for row in c.fetchall()]
    print(50*'#')


def insert_record(unix_rec, datestamp, machineId, cpuPercent, memoryPercent, diskPercent):
    unix_insert = int(time.time())
    c.execute("""
        INSERT INTO receivedData (unix_rec, unix_insert, datestamp, machineId, cpuPercent, memoryPercent, diskPercent)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (unix_rec, unix_insert, datestamp, machineId, cpuPercent, memoryPercent, diskPercent))
    conn.commit()

def read_record_file(filename): # outputs the input file as a list
    file = open("receivedfiles/%s"%filename, "r")
    content = file.read().splitlines()
    file.close()
    os.rename("receivedfiles/%s"%filename, "receivedfiles/used/%s"%filename)  # move file after read
    for i in [0, 2, 3, 4, 5]:
        content[i] = int(content[i])    # convert values to integer
    return content  # returns a list with all the info

def treat_file(filename):   # reads file and inserts it into the database
    data = read_record_file(filename)
    insert_record(data[0], data[1], data[2], data[3], data[4], data[5])

def treat_all_files():   # execute this every 30s or so
    filesToTreat = []   # list with all files to be treated
    for (dirpath, dirnames, filenames) in walk('receivedfiles'):
        filesToTreat.extend(filenames)
        break
    print(filesToTreat)
    for i in filesToTreat:
        treat_file(i)

def del_old(delay=24):  # deletes entries older than delay (in hours)
    current_unix = int(time.time())
    sdelay = 3600*delay # delay in seconds
    oldest = current_unix - sdelay  # oldest unix time allowed
    c.execute('DELETE FROM receivedData WHERE unix_insert < %s' %oldest)
    conn.commit()

def startup():
    create_receivedData_table()
    # create_machineInfo_table()
    update_loop()

def update_loop():
    while True:
        treat_all_files()
        del_old(2)
        read_receivedData()
        time.sleep(20)

startup()
