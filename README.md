## fdsn_station_info ##

This is an ObsPy wrapper script to pull station metadata from IRIS FDSN
server (default server) based on:
1) a time window (required)
2) a search radius based on a center lat/lon (required)
3) network code (optional to refine search)
4) channel codes (optional to refine search)

Returns two files:
1) CSV file at the channel level
2) StationXML file at the response (optional) or channel level (default)

### Purpose/Scope ###

This script has two main uses:
1) Determining the availability of open-access station/channel data
for a particular region and time period. This
information can be fed into another helper script, `fdsn_wf_fetch.py`,
(https://github.com/flyrok/fdsn_wf_fetch) to pull waveforms. This
is the common use of the CSV file, which contains the info needed by
`fdsn_wf_fetch.py`
2) Saving station metadata (including response) as a StationXML file. This
can be read into ObsPy Inventory class, e.g. 
`from obspy import read_inventory`  
`inv = read_inventory("test.staxml")`


## Install ##

Clone source package
`git clone http://github.com/flyrok/fdsn_station_info`

Install with pip after download
`pip install .`

Or install directly from github
`pip install git+https://github.com/flyrok/fdsn_station_info#egg=fdsn_station_info`

Or just call the executable on your PATH can call directly
./fdsn_station_info.py


## Python Dependencies ##

python>=3.6 (script uses f-strings)  
obspy (https://github.com/obspy/obspy/wiki)
-- without this, nothing will work


## Usage/Examples ##

To see help:  
`fdsn_station_info.py --help`    

To see version:  
`fdsn_station_info.py --version`    

To requestion all networks, stations and BH channels for
a particular region and time period:  
`fdsn_station_info.py -b 2019001T00:00 -e 2019100T00:00 --lon -71.2 --lat 42.4 --radmin 1 --radmax 50 -r -c "BH?" -o test.csv`    


