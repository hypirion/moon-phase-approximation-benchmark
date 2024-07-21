#!/usr/bin/env python3

import sys
import datetime
from collections import Counter

def read_data(fname):
  data = []
  with open(fname) as f:
    for line in f:
      ts, phase = line.strip().split()
      ts, phase = datetime.datetime.fromisoformat(ts), int(phase)
      data.append((ts, phase))
  return data

correct = read_data('correct/all-phases.txt')

class Stats:
  def __init__(self, algname, fname):
    self.algname = algname
    approx = read_data(fname)
    if len(correct) != len(approx):
      print(f'{fname}: expected {len(correct)} items, but got {len(approx)}')
      sys.exit(1)

    median = []
    mae_sec = 0.0
    mse_sec = 0.0
    max_err = 0.0
    hour_switch = 0
    day_switches = Counter()

    for i in range(len(approx)):
      ok_ts, ok_phase = correct[i]
      ap_ts, ap_phase = approx[i]
      if ok_phase != ap_phase:
        print('ok_phase is {}, but ap_phase is {}'.format(ok_phase, ap_phase))
      if ok_ts.hour != ap_ts.hour:
        hour_switch += 1

        # take min and move forward by one hour until we hit the other ts
        ok_ts_trunc = ok_ts.replace(minute=0, second=0, microsecond=0)
        ap_ts_trunc = ap_ts.replace(minute=0, second=0, microsecond=0)
        min_ts_trunc = min(ok_ts_trunc, ap_ts_trunc)
        max_ts_trunc = max(ok_ts_trunc, ap_ts_trunc)
        cur_ts = min_ts_trunc
        while cur_ts < max_ts_trunc:
          day_switches[(cur_ts.hour, (cur_ts.hour + 1) %24)] += 1
          cur_ts += datetime.timedelta(hours = 1)
      diff = abs(ok_ts - ap_ts).total_seconds()
      median.append(diff)
      mae_sec += diff
      mse_sec += diff**2
      max_err = max(max_err, diff)

    n = len(correct)
    median.sort()
    if n % 2 == 0:
      self.median = (median[n//2] + median[n//2 + 1])/2
    else:
      self.median = median[n//2 + 1]

    self.mae_sec = mae_sec / n
    self.mse_sec = mse_sec / n
    self.hour_switch = hour_switch / n
    self.max_err = max_err
    max_day_switches = 0
    min_day_switches = 1e10

    for (k, v) in day_switches.items():
      max_day_switches = max(max_day_switches, v/n)
      min_day_switches = min(min_day_switches, v/n)

    self.max_day_switches = max_day_switches
    self.min_day_switches = min_day_switches

  def row_titles(self):
    return ['Algorithm', 'mae (s)', 'mse (s)', 'max err (s)', 'median err (s)', 'hour switches',
            'max day switches', 'min day switches']

  def str_rows(self):
    return (self.algname, f'{self.mae_sec:.0f}', f'{self.mse_sec:.0f}',  f'{self.max_err:.0f}',
            f'{self.median:.0f}', f'{self.hour_switch:.2%}', f'{self.max_day_switches:.2%}',
            f'{self.min_day_switches:.2%}')

synodic = Stats('Synodic', 'synodic/all-phases.txt')
orbital = Stats('Orbital', 'orbital/all-phases.txt')
astronomical = Stats('Astronomical', 'astronomical-algorithms/all-phases.txt')
skyfield = Stats('Skyfield', 'skyfield/all-phases.txt')

def tab_row(content, lens, fillchar = ' '):
  cols = []
  for (c, l) in zip(content, lens):
    cols.append(c.rjust(l, fillchar))
  return '| ' + ' | '.join(cols) + ' |'

def tabulate(title, rows):
  transposed = list(zip(*([title] + rows)))
  lens = [max(len(x) for x in lst) for lst in transposed]
  print(tab_row(title, lens))
  print(tab_row([':']*len(lens), lens, '-'))
  for row in rows:
    print(tab_row(row, lens))

tabulate(synodic.row_titles(), [x.str_rows() for x in [synodic, orbital, astronomical, skyfield]])
