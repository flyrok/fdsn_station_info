#!/usr/bin/env python3

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import argparse
from pathlib import Path
import sys
import math

here = Path(__file__).resolve().parent
exec(open(here / "version.py").read())

def dump_output(inv,output,debug,lon0,lat0):
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
    msg=f" N,   sta, loc,   chan,       lat,        lon,   elev, dist (km),  depth,    sampr,  hang, vang,  sensor\n"
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
                if lat0 is None : lat0=lat
                if lon0 is None: lon0=lon
                dist= latlongdist(lat0,lat,lon0,lon)
                msg=f"{net_code:2s}, {sta_code:>6s}, {loc:>2s}, {code:>6s}, {lat:>9.6f}, {lon:>10.6f}, {elev:>6.1f}, {dist}, {dep:>6.1f}, {sampr:>8.4f}, {az:>5.1f},{dip:>4.1f}, {sensor}\n"

                if debug: print(msg)

                msgs.append(msg)
    file = open(output,"w+")
    for i in msgs:
        file.write(i)
    file.close()

def latlongdist(phi1,phi2,gamma1,gamma2):
    # Calculates distance between 2 points on a sphere
    # Note: Earth is not a perfect sphere, so calculations will have some error

    R = 6371; # Average radius of the earth (km)

    phi1 = math.radians(phi1)
    phi2 = math.radians(phi2)
    gamma1 = math.radians(gamma1)
    gamma2 = math.radians(gamma2)

    phi_dif = phi1-phi2
    gamma_dif = gamma1-gamma2

    a =  math.sin(phi_dif/2)**2+math.cos(phi1)*math.cos(phi2)*math.sin(gamma_dif/2)**2
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = R*c;
    return d

def main():
    '''
    Main routine to collect commandline argumnts and to make fdsn client request
    '''
    parser = argparse.ArgumentParser(prog=progname,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description= '''
            Grab station metadata from IRIS FDSN server for stations that are: 1) within a
            certain search radius of a given lat,lon, and 2) operating during a
            particular time frame. It outputs two files: a CSV file
            and a StationXML file.
            ''',
            epilog='''

            ''')

    parser.add_argument("-b","--begin", type=str,
        required=True, help="Start time in iso-format e.g. 2019001T00:00. Station \
            only operating between begin/endtime will be returned")

    parser.add_argument("-e","--end", type=str,
        required=True, help="End time in iso-format e.g. 2019001T00:00")

    parser.add_argument("-n","--net", type=str,default=None,
        required=False, help="Net code. Used to narrow search results. Multiple network are comma separated and quoted.")

    parser.add_argument("-s","--station", type=str,default=None,
        required=False, help="""Station Codes, defaults to all
            ``ANMO,PFO``. Used if interested in metadata for a particular set stations. 
            Multiple stations are comma separated and quoted  """)

    parser.add_argument("-c","--chan", type=str,default=None,
        required=False, help="""Chan codes, defaults to all available. E.g.
            ``BH?,HH?,*H*``. Used to narrow search results """)

    parser.add_argument("-r","--resp", action="store_true",default=False,
        required=False, help="Set to include response in StationXML file.")

    parser.add_argument("--lon", type=float, default=None,
        required=False, help="Center longitude for search radius. Decimal degrees")

    parser.add_argument("--lat", type=float, default=None,
        required=False, help="Center latitude for search radius. Decimal degrees.")

    parser.add_argument("--radmin", type=float,default=None,
        required=False, help="Minimum search radius in km (>0).")

    parser.add_argument("--radmax", type=float, default=None,
        required=False, help="Maximum search radius in km (>radmin).")

    parser.add_argument("-o","--output", type=str,required=False,
        default="sta_info.csv", help="Output filename for CSV. CSV suffix is replaced with .staxml for StationXML format")

    parser.add_argument("-v", "--verbose", action="count",default=0,
        help="increase debug spewage spewage (e.g. -v, -vv, -vvv)")

    parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()


    # check if lat set then lon set, vice versa 
    if args.lat is not None and args.lon is None: 
        parser.error("--lat requires --lon")
    if args.lon is not None and args.lat is None: 
        parser.error("--lon requires --lat")
    # check if radmax set, then lat/lon set
    if args.radmax is not None and (args.lat is None or args.lon is None):
        parser.error("--radmax requires --lon, --lat")
    # check if lat/lon set then radmax set
    if args.lat and arg.radmax is None:
        parser.error("--lat --lon requires --radmax") 
    # check if radmax is not set then net or station must be set
    if args.radmax is None and (args.net is None and args.station is None):
        parser.error("not setting --radmax requires setting either --net or --station")


    startt= UTCDateTime(args.begin)
    endt= UTCDateTime(args.end)
    net=args.net
    chan=args.chan
    station=args.station
    do_resp=args.resp
    lon=args.lon
    lat=args.lat
    radmin=args.radmin
    radmax=args.radmax
    if radmin: radmin=radmin/111.195
    if radmax: radmax=radmax/111.195
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
        print("station: ",station)
        print("lon:",lon)
        print("lat: ",lat)
        print("radmin: ",radmin)
        print("radmax: ",radmax)
        print("level: ",level)

    client = Client(timeout=240,base_url="http://service.iris.edu")
    if radmax is None:
        if debug > 0:
            print("First try")
        try:
            inv=client.get_stations(starttime=startt,endtime=endt,network=net,channel=chan,
                station=station,level=level)
            dump_output(inv,output,debug, lon, lat)
        except Exception as e:
            print("get_stations fail:",e)
    elif radmax:
        if debug > 0:
            print("Second try")
        try:
            inv=client.get_stations(starttime=startt,endtime=endt,network=net,channel=chan,
                station=station,latitude=lat,longitude=lon,minradius=radmin,maxradius=radmax,level=level)
            dump_output(inv,output,debug, lon, lat)
        except Exception as e:
            print("get_stations fail:",e)

if __name__ == '__main__':
    main()
