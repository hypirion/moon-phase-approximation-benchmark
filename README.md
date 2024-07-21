# Moon Phase Approximation Benchmark

A moon phase approximation benchmark suite, comparing accuracy for different
implementations from 1900 to 2100. The timestamps considered correct are taken
from the [Astronomical Applications Department](https://aa.usno.navy.mil/)'s
API.

All algorithms (except for the orbital one) are implemented in Python.

## Results

|    Algorithm | mae (s) |    mse (s) | max err (s) | median err (s) | hour switches | max day switches | min day switches |
| -----------: | ------: | ---------: | ----------: | -------------: | ------------: | ----------------: | ----------------: |
|      Synodic |   29312 | 1157169588 |       70031 |          28224 |        97.17% |            34.20% |            33.69% |
|      Orbital |     148 |      33071 |         556 |            128 |         3.76% |             0.23% |             0.08% |
| Astronomical |      65 |       5636 |         154 |             63 |         0.96% |             0.06% |             0.01% |
|     Skyfield |      24 |        876 |          80 |             21 |         0.69% |             0.06% |             0.01% |


MAE is the mean absolute error, MSE is the mean squared error, and hour switches
are changes from one hour to another, e.g. 15:59 turning into 16:00 or vice
versa. Day switches are the approximate number of 23:59 -> 00:00 switches, i.e.
the probability of a single moon phase being assigned to the wrong date in a
specific time zone. It is approximate as I don't factor in daylight savings time
switches and don't compute it for 15- and 30- minute time zones.
