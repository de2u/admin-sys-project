# admin-sys-project
A system monitoring program using python (and some bash).

### Sensor
A sensor script using the psutil and shutil libraries for python3.
Creates a file containing system stats on a loop.
Sensor needs to be configured using the sensorcfg.py file (machineId and loop_length).
*disk_usage.sh is an alternative to shutil, we're not using it here*

### Storage
Using the SQLite3 library for python3.
This let's us keep the entire database in one file locally.

**Options:**
* Serverless database storage
* Database backup and recovery

### Web Parser
Returns every alert from [CERT-FR](https://www.cert.ssi.gouv.fr/alerte/) uncluding Title and Link to the alert.
Uses urllib and re libraries.
This function needs more integration to be user friendly.

### Networking
Data files get transferred from the system running the sensor to the one treating the data using the ssh protocol (rsync).
