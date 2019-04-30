#!/bin/bash

starttime=2019001T00:00
endtime=2019300T00:00
lon=-71.0
lat=-41.0
radmin=1
radmax=50
chans="BHZ,BHN,BHE"
output=test.csv

../fdsn_station_info.py -b $starttime -e $endtime -c "$chans" --lon $lon --lat $lat --radmin $radmin --radmax $radmax  -o $output -r
