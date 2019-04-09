import sqlite3
import time
import datetime
import shutil, os

loop_length = 20    # loop length in seconds
start_unix = str(time.time())   # start time

db_name = 'collected_data.db'
conn = sqlite3.connect(db_name,timeout=10) # connection to db
c = conn.cursor()   # cursor creation

def create_receivedData_table():
    # table creation if inexistent
    c.execute('CREATE TABLE IF NOT EXISTS receivedData(unix_rec INTEGER, unix_insert INTEGER, datestamp TEXT, machineId INTEGER, hostname TEXT, machineIp TEXT, cpuPercent REAL, memoryPercent REAL, diskPercent REAL, user TEXT)')

# def create_machineInfo_table():
#     c.execute('CREATE TABLE IF NOT EXISTS machineInfo(machineId REAL, OS TEXT)')

def read_receivedData():
    print(50*'#')
    c.execute('SELECT * FROM receivedData')
    [print(row) for row in c.fetchall()]
    print(50*'#')


def insert_record(unix_rec, datestamp, machineId, hostname, machineIp, cpuPercent, memoryPercent, diskPercent, user):
    unix_insert = int(time.time())
    c.execute("""
        INSERT INTO receivedData (unix_rec, unix_insert, datestamp, machineId, hostname, machineIp, cpuPercent, memoryPercent, diskPercent, user)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (unix_rec, unix_insert, datestamp, machineId, hostname, machineIp, cpuPercent, memoryPercent, diskPercent, user))
    conn.commit()

def read_record_file(filename): # outputs the input file as a list
    file = open("receivedfiles/%s"%filename, "r")
    content = file.read().splitlines()
    file.close()
    os.rename("receivedfiles/%s"%filename, "receivedfiles/used/%s"%filename)  # move file after read
    return content  # returns a list with all the info

def treat_file(filename):   # reads file and inserts it into the database
    data = read_record_file(filename)
    insert_record(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])

def treat_all_files():   # execute this every 30s or so
    filesToTreat = []   # list with all files to be treated
    for (dirpath, dirnames, filenames) in os.walk('receivedfiles'):
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

def db_backup_hourly(name):
    name = name[:-3]
    backup_folder = "dbbackup"
    current_unix = int(time.time())
    if (float(current_unix) - float(start_unix)) % 3600 <= loop_length:

        file_list = os.listdir(backup_folder)
        i = len(file_list)
        for filename in reversed(file_list):
            if i <= 5:
                os.rename(backup_folder + '/' + filename, backup_folder + '/' + name + str(i))
            else:
                os.remove(backup_folder + '/' + filename)
            i -= 1
        shutil.copy(name+'.db', backup_folder)
        os.rename(backup_folder + '/' + name + '.db', backup_folder + '/' +  name + '0')

def startup():
    create_receivedData_table()
    # create_machineInfo_table()
    update_loop()

def update_loop():
    while True:
        treat_all_files()
        del_old(2)
        read_receivedData()
        db_backup_hourly(db_name)
        time.sleep(loop_length)

startup()
