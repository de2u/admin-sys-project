from subprocess import call
import sqlite3


db_name = 'collected_data.db'
conn = sqlite3.connect(db_name,timeout=10) # connection to db
c = conn.cursor()   # cursor creation
c.execute("SELECT DISTINCT user, machineIp FROM receivedData")
ordi = cur.fetchall()

j = len(machine)
for i in range(0, j):
    ip=ordi[i][1]
    user=machine[i][0]
    path="/home/administrator/sensordata/"
    path2="/home/client/sensordata/"
    term=user+"@"+ip+":"+path2

    call(["scp -r", term, path])

    
