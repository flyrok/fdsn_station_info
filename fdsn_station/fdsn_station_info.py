#!/usr/bin/env python3

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import argparse
from pathlib import Path

here = Path(__file__).resolve().parent
exec(open(here / "version.py").read())

def dump_output(inv,output,debug):
    '''
    Dumps station meta data to a text file and an ObsPy Inventory
    The text file does not include the response info that is
    included in the Inventory

    :type  inv: Obspy Inventory 
    :param inv:  This is the inventory returned from
        FDSN server. 

    :type output: str, filename
    :param output: This is the output filename for the human 
        readable text file. For the StationXml file, the
        suffix is replaced with staxml

    :type debug: int, required
    :param debug: specifies debug verbosity
    '''
   
    # Save the inventory as a StationXML file
    xmlout=f"{Path(output).stem}.staxml"
    if debug: print("Saving staxml: ",xmlout)
    inv.write(xmlout,format="STATIONXML")

    msgs=[]
    msg=f"net,sta   ,loc, chan  , lat      ,  lon       , elev  ,  depth,   sampr, cmpaz,cmpinc,sensor\n"
    msgs.append(msg)

    if debug: print(msg)

    # loop through the Inventory and make a human readable text file
    # at the channel level
    for i in range(0,len(inv.networks)): # iter networks
        net=inv.networks[i]
        net_code=net._code
        for j in range(0,len(net)): # iter stations
            sta=net[j]
            sta_code=sta._code
            for k in range(0,len(sta)): # iter chann
                chan=sta[k]
                code=chan._code
                loc=chan._location_code
                lat=chan._latitude
                lon=chan._longitude
                elev=chan._elevation
                dep=chan._depth
                sampr=chan._sample_rate
                az=chan._azimuth
                dip=chan._dip
                sensor=chan.sensor.description
                msg=f"{net_code:2s}, {sta_code:6s}, {loc:2s}, {code:6s}, {lat:9.6f}, {lon:10.6f}, {elev:6.1f}, {dep:6.1f}, {sampr:8.4f}, {az:5.1f},{dip:4.1f}, {sensor}\n"

                if debug: print(msg)

                msgs.append(msg)
    file = open(output,"w+")
    for i in msgs:
        file.write(i)
    file.close() 

def main():
    '''
    Main routine to collect commandline arguemnts and to make fdsn client request
    '''
    parser = argparse.ArgumentParser(prog=progname,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description= '''
            Grab station metadata from IRIS FDSN server for stations that are within a
            certain search radius of a given lat,lon, and where operating during a
            particular time frame. It outputs two files: a human readble CSV file
            and a StationXML file. Th
            ''')

    parser.add_argument("-b","--begin", type=str,
        required=True, help="Start time in iso-format e.g. 2019001T00:00. Station \
            only operating between begin/endtime will be returned")

    parser.add_argument("-e","--end", type=str,
        required=True, help="End time in iso-format e.g. 2019001T00:00")

    parser.add_argument("-n","--net", type=str,default=None,
        required=False, help="Net code. Used to narrow search results. ")

    parser.add_argument("-c","--chan", type=str,default=None,
        required=False, help="Chan codes, wild cards ok default: *")

    parser.add_argument("-r","--resp", action="store_true",default=False,
        required=False, help="set level response otherwise set to channel, default: False")

    parser.add_argument("--lon", type=float,required=True, 
        help="Center longitude for search radius. Decimal degrees.")

    parser.add_argument("--lat", type=float,required=True, 
        help="Center latitude for search radius. Decimal degrees.")

    parser.add_argument("--radmin", type=float,required=True, 
        help="Minimum search radius in km (>0)")

    parser.add_argument("--radmax", type=float,required=True, 
        help="Maximum search radius in km (>radmin)")

    parser.add_argument("-o","--output", type=str,required=False, 
        default="sta_info.csv", help="Output filename for CSV. CSV suffix is replaced with .staxml for StationXML format")

    parser.add_argument("-v", "--verbose", action="count",default=0,
        help="increase debug spewage spewage (e.g. -v, -vv, -vvv)")

    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()

    startt= UTCDateTime(args.begin)
    endt= UTCDateTime(args.end)
    net=args.net
    chan=args.chan
    do_resp=args.resp
    lon=args.lon
    lat=args.lat
    radmin=args.radmin/111.195
    radmax=args.radmax/111.195
    output=args.output
    debug=args.verbose

    if do_resp:
        level='response'
    else:
         level='channel'     

    if debug > 0:
        print('Command line arguments....')
        print("begin: ",startt)
        print("end: ",endt)
        print("net: ",net)
        print("chan: ",chan)
        print("lon:",lon)
        print("lat: ",lat)
        print("radmin: ",radmin)
        print("radmax: ",radmax)
        print("level: ",level)
    
    client = Client(timeout=240,base_url="http://service.iris.edu")
    inv=client.get_stations(starttime=startt,endtime=endt,network=net,channel=chan,
        latitude=lat,longitude=lon,minradius=radmin,maxradius=radmax,level=level)
    dump_output(inv,output,debug)

if __name__ == '__main__':
    main()

