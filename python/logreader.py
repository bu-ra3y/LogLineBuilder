#!/usr/bin/python3
#
# logreader module
# 
# Tool for reading in log lines that report metrics, which look like:
#   key1 val1, key2 val2, key3 val3
#   time 20127837, temp 12.828, mem 1712, altitude 123.22, x 0.212, y 0.1222
#
# Can read from a (file | Python list | serial device) that present log lines, 
#   or a single line/String itself. 
#    
# Parses the lines into a structure useful for working with the metric series
#   data -> 
#     [
#       metric1 -> [val1, val2, val3, val4, ...],
#       metric2 -> [val1, val2, val3, val4, ...],
#       metric3 -> [val1, val2, val3, val4, ...],
#       ...
#     ]
#
#   e.g.:
#   data -> 
#     [
#       'temperature' -> [12, 13, 14, 15, ...],
#       'pressure'    -> [0.1, 0.2, 0.3, 0.4, ...],
#       'memory'      -> [1021, 1022, 1023, 1024, ...],
#       ...
#     ]
#
from collections import defaultdict
import serial
import sys

class LogReader:
  # One piece of state
  data = defaultdict(list)

  # Mainly a debugging function
  def printData(self):
    for key in self.data.keys():
      print("%s: %s" % (key, self.data[key]))
      print("")

  # Read in log lines from a list
  def readList(self, inputList):
    for line in inputList:
      self.readLine(line)

  # Read in log lines from a file
  def readFile(self, filePath):
    with open(filePath) as f:
      for line in f:
        self.readLine(line)

  # Read in log lines from a serial device
  #  Hacky.  Does this in a blocking way / not very useful
  #  Basically will read the Arduino/serial device until you unplug it.
  def readSerial(self, device):
    try: # Catching startup errors witht the Serial device
      with serial.Serial(device, 9600) as ser:
        for i in range(linesToRead):
          try:
            line = ser.readline().decode("utf-8")
            self.readLine(line)
          except:
            print("Boom? Some problem reading the serial device in " \
              "logreader.py. Disconnected? %s" % sys.exc_info()[0])
            break
    except serial.serialutil.SerialException as e:
      print("Boom. Problem starting up serial device. %s" % e)

  # Process a line of data
  # See the notes at the top for what a line looks like
  def readLine(self, line):  
    # iterate over the comma-separated key-value pairs
    for key_value in line.split(","):
      # the split() function may throw excptions 
      #  if it can't split the string.  this can happen when there 
      #   is dirty data - in which case we continue 
      try:
          # split the key and value on whitespace
          key, value = key_value.split()

          # insert the value into the list for the key
          self.data[key].append(float(value))
      except ValueError:
        continue

  # Return all of the data
  # See note at top for what the structure looks like
  def getData(self):
    return self.data

