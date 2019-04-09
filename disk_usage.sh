#!/bin/bash

cd "/home/nas02a/etudiants/inf/uapv1503002/S4/administration systeme/git/sensordata"
disk=$(df /home | awk '{print $5}' | sed "s/%//g" | tail -n1)
file=$(ls -lrt | awk '{print $9}' | tail -1)
echo "$disk" >> $file
