#!/usr/bin/env python3

import json
import urllib.request
import time

aa_link = 'https://aa.usno.navy.mil/api/moon/phases/year?id=hypirion&year={}'

def data_for_year(y):
  with urllib.request.urlopen(aa_link.format(y)) as f:
    return json.load(f)

# want 2011-11-04T00:05:23Z and then moon phase (new, first, full, last)

phase = {
  'New Moon': 0,
  'First Quarter': 1,
  'Full Moon': 2,
  'Last Quarter': 3,
}

def time_and_phase(m):
  return '{year}-{month:02}-{day:02}T{time}:00Z'.format(**m), phase[m['phase']]

data = []

for y in range(1900, 2101):
  cur = data_for_year(y)
  for phase_evt in cur['phasedata']:
    data.append(time_and_phase(phase_evt))
  time.sleep(2)

data.sort()

for (y, phase) in data:
  print('{} {}'.format(y, phase))
