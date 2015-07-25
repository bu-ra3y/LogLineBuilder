#!/usr/bin/python3
#
# logreader module
#  
#
from collections import defaultdict



# This is our data store.
# It is a defaultdict(list) which is a dict with one exception:
#   Whenever a key doesn't exist, it is automatically 
#   initialized with list() (empty list)
# The data lives here as named lists
#       keyA -> (val1, val2, val3, ...)
# e.g.  angle -> (20.1, 19.8, 16.4, 15.2)
#
data = defaultdict(list)

# Mainly a debugging function
def printData():
  for key in data.keys():
    print("%s: %s" % (key, data[key]))
    print("")


# Read in the lines froma file and store them
def readInput(inputFile):
  with open(inputFile) as _inputFile:
    for line in _inputFile:
      # First split the line into key-value pairs
      # The line looks like:
      #   x 1, y 2, z 3.00, r 25.1
      keyValues = line.split(",")
      for key_value in keyValues:
        # split the key and value on whitespace
        key, value = key_value.split()
        # insert the value into the list for the key
        data[key].append(float(value))

# Return all of the data
def getData():
  return data