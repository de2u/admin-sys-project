import psutil   # 'python3 -m pip install psutil' on windows
import time
import datetime
import shutil
from sensorcfg import *

def write_to_file(filename):
    f = open(str(filename), "w+")   # opening/creating file for writing
    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y %m %d %H:%M:%S'))
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()[2]
    disk_total, disk_used, disk_free = shutil.disk_usage("\\")
    disk_percent = "%.1f" % (disk_used/disk_total*100)
    f.write(str(unix)+'\n'+date+'\n'+str(machineId)+'\n'+str(cpu)+'\n'+str(mem)+'\n'+str(disk_percent))
    f.close()

def main():
    write_to_file(12345)

main()
