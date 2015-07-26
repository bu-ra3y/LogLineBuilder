#!/usr/bin/python3
# test logreader
from logreader import LogReader

### Example 1 ########################################################
# Let's input some log lines, just from strings
#  This is a nice self-contained example, further below for a file example
line1 = "pan 12, tilt 15.0"
line2 = "pan 13, tilt 16.0"
line3 = "pan 14, tilt 20.0"
line4 = "pan 16, tilt 21.0"
line5 = "pan 18, tilt 20.0"

l = LogReader()
l.readLine(line1)
l.readLine(line2)
l.readLine(line3)
l.readLine(line4)
l.readLine(line5)

# Now let's see the series of data we have for each metric
for metric in l.getData():
  print("%s: %s" % (metric, l.getData()[metric]))
