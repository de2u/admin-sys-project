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
    c.execute('CREATE TABLE IF NOT EXISTS receivedData(unix_rec REAL, unix_insert REAL, datestamp TEXT, machineId REAL, cpuPercent REAL, memoryPercent REAL, diskPercent REAL)')

def create_machineInfo_table():
    c.execute('CREATE TABLE IF NOT EXISTS machineInfo(machineId REAL, OS TEXT)')

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

def treat_data(filename):   # reads file and inserts it into the database
    data = read_record_file(filename)
    insert_record(data[0], data[1], data[2], data[3], data[4], data[5])

def treatment_loop():   # execute this every 30s or so
    filesToTreat = []
    for (dirpath, dirnames, filenames) in walk('receivedfiles'):
        filesToTreat.extend(filenames)
        break
    print(filesToTreat)
    for i in filesToTreat:
        treat_data(i)

create_receivedData_table()
treatment_loop()
