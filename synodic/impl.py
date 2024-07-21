#!/usr/bin/env python3

import datetime

reference_ts = datetime.datetime(2001, 1, 1, 0, 0, 0, 0, datetime.UTC)

def ts_to_lun(ts):
  diff = ts - reference_ts
  days = diff.days + diff.seconds/86400
  lun = 0.20439731 + days*0.03386319269
  return lun

def lun_to_ts(lun):
  days = (lun - 0.20439731)/0.03386319269
  diff = datetime.timedelta(days = days)
  ts = reference_ts + diff
  return ts

def next_phase_lun(ts):
  l = ts_to_lun(ts)
  lmod = l % 1
  if lmod < 0.25:
    return l - lmod + 0.25
  elif lmod < 0.5:
    return l - lmod + 0.5
  elif lmod < 0.75:
    return l - lmod + 0.75
  else:
    return l - lmod + 1.0

def lun_to_phase(lun):
  return round((lun % 1)*4)

week = datetime.timedelta(hours = 7*24)
accuracy = datetime.timedelta(seconds = 30)

start_ts = datetime.datetime(1900, 1, 1, 0, 0, 0, 0, datetime.UTC)
end_ts = datetime.datetime(2101, 1, 1, 0, 0, 0, 0, datetime.UTC)

cur_lun = next_phase_lun(start_ts)
cur_ts = lun_to_ts(cur_lun)

i = 0
while cur_ts < end_ts:
  print(cur_ts.strftime('%Y-%m-%dT%H:%M:%SZ'), lun_to_phase(cur_lun))
  cur_lun += 0.25
  cur_ts = lun_to_ts(cur_lun)
