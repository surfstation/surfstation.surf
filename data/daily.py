#!/usr/bin/env python3
import json
import sys
import datetime
from dateutil import tz

new_york_time = tz.gettz('America/New_York')
now = datetime.datetime.now(new_york_time)
tomorrow = now + datetime.timedelta(days = 1)

now_str = now.strftime('%Y-%m-%d')
tomorrow_str = tomorrow.strftime('%Y-%m-%d')

result = {'tides': [], 'tides_tomorrow': []}

with open(sys.argv[1] + 'tides.txt', 'r') as f:
  for line in f:
    fields = line.split()
    if fields[0] == now_str:
      result['tides'].append(fields[1] + ' ' + fields[2] + ' ' + fields[3])
    if fields[0] == tomorrow_str:
      result['tides_tomorrow'].append(fields[1] + ' ' + fields[2] + ' ' + fields[3])

with open(sys.argv[1] + 'firstlight.txt', 'r') as f:
  for line in f:
    if line.startswith(now_str):
      result['firstLight'] = datetime.datetime.fromisoformat(line[:-1]).astimezone(new_york_time).strftime('%I:%M %p')

with open(sys.argv[1] + 'sunrise.txt', 'r') as f:
  for line in f:
    if line.startswith(now_str):
      result['sunrise'] = datetime.datetime.fromisoformat(line[:-1]).astimezone(new_york_time).strftime('%I:%M %p')

with open(sys.argv[1] + 'sunset.txt', 'r') as f:
  for line in f:
    if line.startswith(now_str):
      result['sunset'] = datetime.datetime.fromisoformat(line[:-1]).astimezone(new_york_time).strftime('%I:%M %p')

with open(sys.argv[1] + 'lastlight.txt', 'r') as f:
  for line in f:
    if line.startswith(now_str):
      result['lastLight'] = datetime.datetime.fromisoformat(line[:-1]).astimezone(new_york_time).strftime('%I:%M %p')

with open(sys.argv[2], 'w') as f:
  f.write(json.dumps(result, sort_keys=False, indent=2))
