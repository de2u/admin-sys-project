from subprocess import Popen
import sqlite3

def recup():
	db_name = 'collected_data.db'
	conn = sqlite3.connect(db_name,timeout=10) # connection to db
	c = conn.cursor()   # cursor creation
	c.execute("SELECT DISTINCT user, machineIp FROM receivedData")
	ordi = c.fetchall()

	j = len(ordi)
	for i in range(0, j):
    	ip=ordi[i][1]
    	user=ordi[i][0]
    	path="/home/administrator/receivedfiles"
    	path2="/home/"+user+"/sensordata/*"
    	term=user+"@"+ip+":"+path2
    	cmd= "rsync --remove-source-files -e ssh "+term+" "+path
    	Popen(cmd, shell=True)

    
