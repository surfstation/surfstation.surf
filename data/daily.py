#!/usr/bin/env python3
import json
import re
import requests
import sys
import datetime

# api references:
# https://api.sunrise-sunset.org/json?lat=29.84&lng=-81.26&formatted=0

result = {'tides': []}

now = datetime.datetime.now().strftime('%Y-%m-%d')

with open(sys.argv[1], 'r') as f:
  for line in f:
    fields = line.split()
    if fields[0] == now:
      result['tides'].append(fields[1] + ' ' + fields[2] + ' ' + fields[3])

headers = {
  'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
}

params = {
  'lat': '29.84',
  'lng': '-81.26',
  'formatted': '0',
}

r = requests.get('https://api.sunrise-sunset.org/json', headers=headers, params=params, timeout=60, verify=True)

print(r.url)

if r.status_code == 200:
  data = r.json()
  if data['status'] == 'OK':
    result['firstLight'] = datetime.datetime.fromisoformat(data['results']['nautical_twilight_begin']).astimezone().strftime('%I:%M %p')
    result['sunrise'] = datetime.datetime.fromisoformat(data['results']['sunrise']).astimezone().strftime('%I:%M %p')
    result['sunset'] = datetime.datetime.fromisoformat(data['results']['sunset']).astimezone().strftime('%I:%M %p')
    result['lastLight'] = datetime.datetime.fromisoformat(data['results']['nautical_twilight_end']).astimezone().strftime('%I:%M %p')

with open(sys.argv[2], 'w') as f:
  f.write(json.dumps(result, sort_keys=False, indent=2))
