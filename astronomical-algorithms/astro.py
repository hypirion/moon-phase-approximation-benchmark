#!/usr/bin/env python3

# Inspired by
# https://www.celestialprogramming.com/moonphases.html

import datetime
import sys
from math import tau, sin, cos, floor, trunc

def cycle_estimate(year, month):
  year_frac = (month * 30 + 15)/365
  k = 12.3685*((year + year_frac) - 2000)
  return floor(k)

def phase_date(cycle, phase):
  k = cycle + phase/4
  T = k/1236.85
  JDE = 2451550.09766 + 29.530588861*k + 0.00015437*T*T - 0.000000150*T*T*T + 0.00000000073*T*T*T*T
  E = 1 - 0.002516*T - 0.0000074*T*T

  M = (0.04456523712042321 + 0.5079843043823915*k - 2.443460952792061e-08*T*T - 1.9198621771937627e-09*T*T*T) % tau
  Mp = (3.5179606894776065 + 6.73377583058987*k + 0.00018776601158805397*T*T + 2.16071761396898e-07*T*T*T - 1.0122909661567113e-09*T*T*T*T) % tau
  F = (2.804932603514103 + 6.818486564979858*k - 2.8131216883644604e-05*T*T - 3.9618974020271276e-08*T*T*T + 1.9198621771937624e-10*T*T*T*T) % tau
  Om = (2.177727592858917 - 0.027292688803421346*k + 3.607944629722678e-05*T*T + 3.7524578917878086e-08*T*T*T) % tau

  A1 = (5.231973498703401 + 0.0018746232429820695*k - 0.00016009905228543987*T*T) % tau
  A2 = (4.396135319923317 + 0.0002848551872179945*k) % tau
  A3 = (4.39526265529732 + 0.46516316256618145*k) % tau
  A4 = (6.098529472318587 + 0.6355176299099998*k) % tau
  A5 = (1.4775957447383994 + 0.3177588149549999*k) % tau
  A6 = (2.473829681776763 + 0.9303263076790703*k) % tau
  A7 = (3.615275012581054 + 0.0428257023615455*k) % tau
  A8 = (2.70246781378802 + 0.12752876498227286*k) % tau
  A9 = (0.6024876577884426 + 0.47579837872308645*k) % tau
  A10 = (3.6161476772070515 + 0.002126229907949572*k) % tau
  A11 = (5.0848422427602795 + 0.032190486204640496*k) % tau
  A12 = (2.8225464663252295 + 0.4223374602046359*k) % tau
  A13 = (4.181110756077616 + 0.4452875799372728*k) % tau
  A14 = (5.7866391349872 + 0.06270126753716165*k) % tau

  if phase == 0:
    correction = (0.00002*sin(4*Mp) + -0.00002*sin(3*Mp + M) + -0.00002*sin(Mp - M - 2*F) + 0.00003*sin(Mp - M + 2*F) + -0.00003*sin(Mp + M + 2*F) + \
                0.00003*sin(2*Mp + 2*F) + 0.00003*sin(Mp + M - 2*F) + 0.00004*sin(3*M) + 0.00004*sin(2*Mp - 2*F) + -0.00007*sin(Mp + 2*M) + -0.00017*sin(Om) + \
                -0.00024*E*sin(2*Mp - M) + 0.00038*E*sin(M - 2*F) + 0.00042*E*sin(M + 2*F) + -0.00042*sin(3*Mp) + 0.00056*E*sin(2*Mp + M) + -0.00057*sin(Mp + 2*F) + \
                -0.00111*sin(Mp - 2*F) + 0.00208*E*E*sin(2*M) + -0.00514*E*sin(Mp + M) + 0.00739*E*sin(Mp - M) + 0.01039*sin(2*F) + 0.01608*sin(2*Mp) + \
                0.17241*E*sin(M) + -0.40720*sin(Mp))
  if phase in [1, 3]:
    correction = (-0.00002*sin(3*Mp + M) + 0.00002*sin(Mp - M + 2*F) + 0.00002*sin(2*Mp - 2*F) + 0.00003*sin(3*M) + 0.00003*sin(Mp + M - 2*F) + 0.00004*sin(Mp - 2*M) +
                -0.00004*sin(Mp + M + 2*F) + 0.00004*sin(2*Mp + 2*F) + -0.00005*sin(Mp - M - 2*F) + -0.00017*sin(Om) + 0.00027*E*sin(2*Mp + M) + -0.00028*E*E*sin(Mp + 2*M) +
                0.00032*E*sin(M - 2*F) + 0.00032*E*sin(M + 2*F) + -0.00034*E*sin(2*Mp - M) + -0.00040*sin(3*Mp) + -0.00070*sin(Mp + 2*F) + -0.00180*sin(Mp - 2*F) +
                0.00204*E*E*sin(2*M) + 0.00454*E*sin(Mp - M) + 0.00804*sin(2*F) + 0.00862*sin(2*Mp) + -0.01183*E*sin(Mp + M) + 0.17172*E*sin(M) + -0.62801*sin(Mp))
    W = 0.00306 - 0.00038*E*cos(M) + 0.00026*cos(Mp) - 0.00002*cos(Mp - M) + 0.00002*cos(Mp + M) + 0.00002*cos(2*F)

    if phase == 1:
      correction += W
    else:
      correction -= W
  if phase == 2:
    correction = (0.00002*sin(4*Mp) + -0.00002*sin(3*Mp + M) + -0.00002*sin(Mp - M - 2*F) + 0.00003*sin(Mp - M + 2*F) + -0.00003*sin(Mp + M + 2*F) + 0.00003*sin(2*Mp + 2*F) +
                0.00003*sin(Mp + M - 2*F) + 0.00004*sin(3*M) + 0.00004*sin(2*Mp - 2*F) + -0.00007*sin(Mp + 2*M) + -0.00017*sin(Om) + -0.00024*E*sin(2*Mp - M) +
                0.00038*E*sin(M - 2*F) + 0.00042*E*sin(M + 2*F) + -0.00042*sin(3*Mp) + 0.00056*E*sin(2*Mp + M) + -0.00057*sin(Mp + 2*F) + -0.00111*sin(Mp - 2*F) +
                0.00209*E*E*sin(2*M) + -0.00514*E*sin(Mp + M) + 0.00734*E*sin(Mp - M) + 0.01043*sin(2*F) + 0.01614*sin(2*Mp) + 0.17302*E*sin(M) + -0.40614*sin(Mp))

  JDE += correction

  correction = (0.000325*sin(A1) + 0.000165*sin(A2) + 0.000164*sin(A3) + 0.000126*sin(A4) + 0.000110*sin(A5) + 0.000062*sin(A6) + 0.000060*sin(A7) +
            0.000056*sin(A8) + 0.000047*sin(A9) + 0.000042*sin(A10) + 0.000040*sin(A11) + 0.000037*sin(A12) + 0.000035*sin(A13) + 0.000023*sin(A14))
        
  JDE += correction
  return julian_to_gregorian(JDE)

def julian_to_gregorian(jd):
  tmp = jd + 0.5
  Z = trunc(tmp)
  F = tmp - Z
  A = Z
  if Z >= 2299161:
    alpha = trunc((Z - 1867216.25)/36524.25)
    A = Z + 1 + alpha - trunc(alpha/4)

  B = A+1524
  C = trunc((B - 122.1)/365.25)
  D = trunc(365.25*C);
  E = trunc((B - D)/30.6001);

  day = B-D-trunc(30.6001*E)+F;
  month = E-1;
  if E > 13:
    month = E - 13
  year = C-4716;
  if month < 3:
    year = C-4715

  day_frac = day % 1
  day = trunc(day)
  hour = trunc(day_frac * 24)
  hour_frac = (day_frac * 24) % 1
  minute = trunc(hour_frac * 60)
  minute_frac = (hour_frac * 60) % 1
  sec = trunc(minute_frac * 60)

  return datetime.datetime(year, month, day, hour, minute, sec, 0, datetime.UTC)

def phases_in_interval(start_year, end_year):
  k = cycle_estimate(start_year, 0) - 1
  while True:
    for phase in range(0, 4):
      ts = phase_date(k, phase)
      if start_year <= ts.year <= end_year:
        print(ts.strftime('%Y-%m-%dT%H:%M:%SZ'), phase)
    if end_year < ts.year:
      break
    k += 1

phases_in_interval(1900, 2100)
