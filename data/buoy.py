#!/usr/bin/env python3
import json
import re
import requests
import xml.etree.ElementTree as ET
import sys
import datetime
from dateutil import tz

# https://www.ndbc.noaa.gov/station_page.php?station=41117
# https://www.ndbc.noaa.gov/data/latest_obs/41117.rss

result = {'buoy': {}}

headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

r = requests.get('https://www.ndbc.noaa.gov/data/latest_obs/41117.rss', headers=headers, timeout=60, verify=True)

print(r.url)

new_york_time = tz.gettz('America/New_York')
now = datetime.datetime.now().replace(microsecond=0).isoformat()

if r.status_code == 200:
  root = ET.fromstring(r.content)
  data = root.findall('./channel/item/description')[0].text
  match = re.match(r'.*<strong>Significant Wave Height:</strong>\s+(\d+\.\d+)\s+ft', data, re.DOTALL | re.IGNORECASE)
  if match:
    result['buoy']['swell_height_feet'] = match[1]
  match = re.match(r'.*<strong>Average Period:</strong>\s+(\d+\.\d+)\s+sec', data, re.DOTALL | re.IGNORECASE)
  if match:
    result['buoy']['swell_period_secs'] = match[1]
  match = re.match(r'.*<strong>Mean Wave Direction:</strong>.*\((\d+)&#176;\)', data, re.DOTALL | re.IGNORECASE)
  if match:
    result['buoy']['swell_angle_degrees'] = match[1]
  match = re.match(r'.*<strong>Water Temperature:</strong>\s+(\d+\.\d+)&#176;F\s+', data, re.DOTALL | re.IGNORECASE)
  if match:
    result['buoy']['temperature_fahrenheit'] = match[1]
  result['buoy']['when'] = datetime.datetime.strptime(root.findall('./channel/item/pubDate')[0].text, '%a, %d %b %Y %H:%M:%S %z').astimezone(new_york_time).strftime('%m/%d/%Y %I:%M %p')
  result['buoy']['timestamp'] = now
  with open(sys.argv[1], 'w') as f:
    f.write(json.dumps(result, sort_keys=False, indent=2))
