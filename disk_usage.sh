#!/bin/bash

cd "/home/client/sensordata"
disk=$(df /home | awk '{print $5}' | sed "s/%//g" | tail -n1)
file=$(ls -lrt | awk '{print $9}' | tail -1)
echo "$disk" >> $file
