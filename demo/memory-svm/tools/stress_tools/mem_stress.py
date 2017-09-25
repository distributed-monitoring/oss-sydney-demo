import sys
import subprocess
import time
import math

args = sys.argv

if len(args) != 5:
    print 'Usage: Bytes Counts Interval_sec Stress_keep_time'
    sys.exit(1)

[_, membytes, counts_str, interval_str, keeptime_str] = args

counts = int(counts_str)
interval = float(interval_str)
keeptime = int(keeptime_str)

for timestep in [interval*t+keeptime for t in range(counts-1, -1, -1)]:
    cmd = 'stress -m 1 --vm-bytes '
    cmd += membytes
    cmd += ' --vm-keep -t '
    cmd += str(math.ceil(timestep))
    cmd += ' &'
    subprocess.call(cmd, shell=True)
    time.sleep(interval)

time.sleep(1)
print 'Stress keep...'
time.sleep(keeptime)

print 'OK'
