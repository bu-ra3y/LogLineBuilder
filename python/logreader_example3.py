#!/usr/bin/python3
# test logreader
from logreader import LogReader

### Example 3 ########################################################
# Now an example, reading from a serial device 
#  The serial device we'll use is "/dev/cu.usbmodem1411"
# Try plugging in an Arduino that is using LogLineBuilder
#  and letting this read data for a bit and then unplug the Arduino
#  serial connection
#
device="/dev/cu.usbmodem1411"

l = LogReader()
print("Starting to listen to serial device on %s" % device)
l.readSerial(device)
print("Done reading")

# Now let's see the series of data we have for each metric
for metric in l.getData():
  print("%s: %s" % (metric, l.getData()[metric]))
