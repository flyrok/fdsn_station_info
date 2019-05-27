SET starttime=2019001T00:00

SET endtime=2019300T00:00

SET lon=-71.2

SET lat=42.4

SET radmin=1
SET radmax=50
SET chans=BH?

SET output=test/test2.csv
python fdsn_station_info.py -b %starttime% -e %endtime% -c %chans% --lon %lon% --lat %lat% --radmin %radmin% --radmax %radmax% -o %output% -r -v
pause