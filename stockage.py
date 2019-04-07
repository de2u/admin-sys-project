import sqlite3
import time
import datetime
import os

db_name = 'collected_data.db'
conn = sqlite3.connect(db_name) # connection to db
c = conn.cursor()   # cursor creation

def create_receivedData_table():
    # table creation if inexistent
    c.execute('CREATE TABLE IF NOT EXISTS receivedData(unix_rec REAL, unix_insert REAL, datestamp TEXT, machineId REAL, cpuPercent REAL, memoryPercent REAL, diskPercent REAL)')

def create_machineInfo_table():
    c.execute('CREATE TABLE IF NOT EXISTS machineInfo(machineId REAL, OS TEXT)')

def insert_record(unix_rec, datestamp, machineId, cpuPercent, memoryPercent, diskPercent):
    unix_insert = time.time()
    c.execute("""
        INSERT INTO receivedData (unix_rec, unix_insert, datestamp, machineId, cpuPercent, memoryPercent, diskPercent)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (unix_rec, unix_insert, datestamp, machineId, cpuPercent, memoryPercent, diskPercent))
    conn.commit()

def read_record_file(filename):
    file = open("receivedfiles/%s"%filename, "r")
    content = file.read().splitlines()
    file.close()
    # os.rename("receivedfiles/%s"%filename, "receivedfiles/used/%s"%filename)
    for i in [0, 2, 3, 4, 5]:
        content[i] = int(content[i])
    return content

print(read_record_file('testinput1.txt'))
