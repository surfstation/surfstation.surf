#!/usr/bin/env python3
import json
import re
import requests
import sys
import datetime
from dateutil import tz

new_york_time = tz.gettz('America/New_York')
now = datetime.datetime.now(new_york_time)
tomorrow = now + datetime.timedelta(days = 1)

now_str = now.strftime('%Y-%m-%d')
tomorrow_str = tomorrow.strftime('%Y-%m-%d')

# api references:
# https://api.sunrise-sunset.org/json?lat=29.84&lng=-81.26&formatted=0

result = {'tides': [], 'tides_tomorrow': []}

with open(sys.argv[1], 'r') as f:
  for line in f:
    fields = line.split()
    if fields[0] == now_str:
      result['tides'].append(fields[1] + ' ' + fields[2] + ' ' + fields[3])
    if fields[0] == tomorrow_str:
      result['tides_tomorrow'].append(fields[1] + ' ' + fields[2] + ' ' + fields[3])

headers = {
  'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
}

params = {
  'lat': '29.84',
  'lng': '-81.26',
  'formatted': '0',
}

r = requests.get('https://api.sunrise-sunset.org/json', headers=headers, params=params, timeout=60, verify=False)

print(r.url)

if r.status_code == 200:
  data = r.json()
  if data['status'] == 'OK':
    result['firstLight'] = datetime.datetime.fromisoformat(data['results']['nautical_twilight_begin']).astimezone(new_york_time).strftime('%I:%M %p')
    result['sunrise'] = datetime.datetime.fromisoformat(data['results']['sunrise']).astimezone(new_york_time).strftime('%I:%M %p')
    result['sunset'] = datetime.datetime.fromisoformat(data['results']['sunset']).astimezone(new_york_time).strftime('%I:%M %p')
    result['lastLight'] = datetime.datetime.fromisoformat(data['results']['nautical_twilight_end']).astimezone(new_york_time).strftime('%I:%M %p')

with open(sys.argv[2], 'w') as f:
  f.write(json.dumps(result, sort_keys=False, indent=2))

now_str = now.strftime('%Y%m%d')

params = {
  'product': 'predictions',
  'application': 'NOS.COOPS.TAC.WL',
  'begin_date': now_str,
  'end_date': now_str,
  'datum': 'MLLW',
  'station': '8720587',
  'time_zone': 'lst_ldt',
  'units': 'english',
  'interval': 'h',
  'format': 'json',
}

r = requests.get('https://tidesandcurrents.noaa.gov/api/datagetter', headers=headers, params=params, timeout=60, verify=False)

print(r.url)

if r.status_code == 200:
  with open(sys.argv[3], 'w') as f:
    f.write(r.text)
