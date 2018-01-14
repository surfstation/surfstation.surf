#!/usr/bin/env python3
import json
import re
import requests
import sys

# api references:
# http://aa.usno.navy.mil/data/docs/api.php
# https://tidesandcurrents.noaa.gov/api/

result = {'tides': []}

phen_decode = {
  'BC': 'firstLight',
  'R': 'sunrise',
  'U': 'midday',
  'S': 'sunset',
  'EC': 'lastLight',
}

highlow_decode = {
  'L': 'Low',
  'H': 'High',
}

headers = {
  'User-Agent': 'TheSurfStationSurfReport/1.0',
}

params = {
  'ID': 'SURFSTAT',
  'date': 'today',
  'loc': 'St. Augustine, FL',
  'format': 'json',
}

r = requests.get('http://api.usno.navy.mil/rstt/oneday', headers=headers, params=params, timeout=60)

if r.status_code == 200:
  data = r.json()
  if not data['error']:
    result['moonStatus'] = data['fracillum'] + ' - ' + data['curphase']
    rgx = re.compile(r'\s*([ap]\.m\.).*', re.IGNORECASE)
    for phenomena in data['sundata']:
      if phenomena['phen'] in phen_decode:
        result[phen_decode[phenomena['phen']]] = rgx.sub(r' \1', phenomena['time'].upper()).replace('.', '')

params = {
  'station': '8720587',
  'date': 'today',
  'product': 'predictions',
  'datum': 'MLLW',
  'units': 'english',
  'time_zone': 'lst_ldt',
  'format': 'json',
  'interval': 'hilo',
  'application': 'SURFSTAT',
}

r = requests.get('https://tidesandcurrents.noaa.gov/api/datagetter', headers=headers, params=params, timeout=60)

if r.status_code == 200:
  data = r.json()
  rgx = re.compile(r'.*\s+', re.IGNORECASE)
  for prediction in data['predictions']:
    time_split = rgx.sub(r'', prediction['t']).split(':')
    temp_hour = int(time_split[0], 10)
    ampm = 'AM' if temp_hour < 12 else 'PM'
    temp_hour = temp_hour - 12 if temp_hour > 12 else 12 if temp_hour == 0 else temp_hour
    result['tides'].append(str(temp_hour) + ':' + time_split[1] + ' ' + ampm + ' ' + highlow_decode[prediction['type']])

with open(sys.argv[1], 'w') as f:
  f.write(json.dumps(result, sort_keys=False, indent=2))
