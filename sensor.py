import psutil   # 'python3 -m pip install psutil' on windows
import shutil
import os
import time
import datetime
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
    print(str(unix)+'\n'+date+'\n'+str(machineId)+'\n'+str(cpu)+'\n'+str(mem)+'\n'+str(disk_percent))

def main():
    fileId = 1
    if not os.path.exists(sensor_data_folder):
        os.mkdir(sensor_data_folder)
    while True:
        filename = sensor_data_folder + '/' + str(machineId) + '_' + hex(fileId)
        print('\n\n' + filename + ':\n')
        write_to_file(filename)
        fileId += 1
        time.sleep(loop_length)

main()
