## fdsn_station_info ##

This is a ObsPy wrapper script to pull station metadata from IRIS FDSN
server (default server) based on:
1) a time window (required)
2) a search radius based on a center lat/lon (required)
3) network code (optional to refine search)
4) channel codes (optional to refine search)

Returns two files:
1) CSV file at the channel level
2) StationXML file at the response (optional) or channel level (default)


## Install ##

To get the source code
**git clone ...**  

To install with pip 

**pip3 install . **  


## Python Dependencies ##

obspy -- without this, nothing will work

## Usage/Examples ##

To see help:  
**fdsn_station_info.py --help**    

To see version:  
**fdsn_station_info.py --version**    

To requestion all networks, stations and BH channels:  
**fdsn_station_info.py -b 2019001T00:00 -e 2019100T00:00 --lon -71.2 --lat 42.4 --radmin 1 --radmax 50 -r -c "BH?" -o test.csv**    


