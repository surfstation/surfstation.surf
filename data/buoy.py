#!/usr/bin/env python3
import json
import re
import requests
import xml.etree.ElementTree as ET
import sys
import datetime
from dateutil import tz

# http://cdip.ucsd.edu/m/products/?stn=194p1
# https://cdip.ucsd.edu/rss/194.xml

result = {'buoy': {}}


headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
}

r = requests.get('https://cdip.ucsd.edu/rss/194.xml', headers=headers, timeout=60, verify=True)

print(r.url)

new_york_time = tz.gettz('America/New_York')
now = datetime.datetime.now().replace(microsecond=0).isoformat()

if r.status_code == 200:
  root = ET.fromstring(r.content)
  data = root.findall('./channel/item/description')[0].text
  result['buoy']['swell_height_feet'] = re.match(r'.*<strong>height</strong>.*\((\d+\.\d+)\s+feet\)', data, re.DOTALL | re.IGNORECASE)[1]
  result['buoy']['swell_period_secs'] = re.match(r'.*<strong>period</strong>\s+(\d+\.\d+)\s+seconds', data, re.DOTALL | re.IGNORECASE)[1]
  result['buoy']['swell_angle_degrees'] = re.match(r'.*<strong>direction</strong>\s+(\d+)\s+degrees', data, re.DOTALL | re.IGNORECASE)[1]
  result['buoy']['temperature_fahrenheit'] = re.match(r'.*<strong>sea\s+surface\s+temp</strong>.*\((\d+\.\d+)\s+F\)', data, re.DOTALL | re.IGNORECASE)[1]
  result['buoy']['when'] = datetime.datetime.strptime(root.findall('./channel/pubDate')[0].text, '%a, %d %b %Y %H:%M:%S %z').astimezone(new_york_time).strftime('%m/%d/%Y %I:%M %p')
  result['buoy']['timestamp'] = now
  with open(sys.argv[1], 'w') as f:
    f.write(json.dumps(result, sort_keys=False, indent=2))
