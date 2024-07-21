#!/usr/bin/env python3

from skyfield import almanac
from skyfield.api import N, S, E, W, load, wgs84
from math import pi, sin, cos, floor

ts = load.timescale()
eph = load('de440s.bsp')

t0 = ts.utc(1900, 1, 1)
t1 = ts.utc(2100, 12, 31)
t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))

def fmt_ts(ts):
  return ts.utc_datetime().strftime('%Y-%m-%dT%H:%M:%SZ')

for (ts, phase) in zip(t, y):
  print(fmt_ts(ts), phase)

