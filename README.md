# fdsn_station_info

Pull station meta data from IRIS FDSN server (default) based on
1) a time window (required)
2) a search radius based on a center lat/lon (required)
3) network code (optional)
4) channel codes (optional)

Returns two files:
1) CSV file at the channel level
2) StationXML file at the response (option) or channel level (default)


# Install

git clone ...  

To install in editable mode  

pip3 install -e .  

# Python Dependencies

argparse  
obspy

# Usage

to see help:  
fdsn_station_info.py --help  

To see version:  
fdsn_station_info.py --version

To requestion all network and BH channels:  
fdsn_station_info.py -b 2019001T00:00 -e 2019100T00:00 --lon -71.0 --lat 41.0 --radmin 1 --radmax 50 -r -c "BH*" -o test.csv


