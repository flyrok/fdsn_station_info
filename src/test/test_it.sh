#!/bin/bash

starttime=2019001T00:00
endtime=2019300T00:00
lon=-71.2
lat=42.4
radmin=1
radmax=50
chans=BH?
output=test.csv

../fdsn_station_info.py -b $starttime -e $endtime -c $chans --lon $lon --lat $lat --radmin $radmin --radmax $radmax  -o $output -r -v
