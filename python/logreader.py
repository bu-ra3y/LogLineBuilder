#!/usr/bin/python3
#
# logreader module
#  
#
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial


# This is our data store.
# It is a defaultdict(list) which is a dict with one exception:
#   Whenever a key doesn't exist, it is automatically 
#   initialized with list() (empty list)
# The data lives here as named lists
#       keyA -> (val1, val2, val3, ...)
# e.g.  angle -> (20.1, 19.8, 16.4, 15.2)
#
data = defaultdict(list)

# This is where we keep track of the lines we're drawing
lines = list()

# and the set of axes
axes_array = ()

figure = None
viewSize = 200

# Are we debugging? (print stuff out)
DEBUG = False

# A simple method to only print something if debugging
def debug(message, argumentList):
  if(DEBUG):
    print(message % argumentList)

# Mainly a debugging function
def printData():
  for key in data.keys():
    print("%s: %s" % (key, data[key]))
    print("")

# Read in raw lines from a list
def readInList(inputList):
  for line in inputList:
    processLine(line)

# Read in raw lines from a file
def readInFile(inputFile):
  with open(inputFile) as f:
    for line in f:
      processLine(line)

# Read in raw lines from a serial device
#  only reads in linesToRead lines (hacky!)
def readInSerial(device, linesToRead):
  with serial.Serial(device, 9600) as ser:
    for i in range(linesToRead):
      line = ser.readline().decode("utf-8")
      processLine(line)

# Process a line of data
# The line is comma-separated key-value, string-float pairs like:
#   x 1, y 2, z 3.00, r 25.1
def processLine(line):  
  # iterate over the comma-separated key-value pairs
  for key_value in line.split(","):
    # the split() function may throw excptions 
    #  if it can't split the string.  this can happen when there 
    #   is dirty data - in which case we continue 
    try:
        # split the key and value on whitespace
        key, value = key_value.split()

        # insert the value into the list for the key
        data[key].append(float(value))
    except ValueError:
      continue

# Return all of the data
def getData():
  return data

# Plot the data, live, reading from a serial port
def plotDataLiveFromSerial(pathToSerialDevice, plotConfig):
  with serial.Serial(pathToSerialDevice, 9600) as ser:
    processConfig(plotConfig)
    animation.FuncAnimation(figure, update, fargs=[ser])
    plt.show()



# Chart the data using MatPlotLib
def plotData(config):
  # config contains 1 item for each intended subplot.
  #  thus, the length of config should tell us how many subplots we want
  num_subplots = len(config)
  
  # Create a figure with several subplots
  #  number of subplots according to the config
  #  all subplots share the temporal axis (x)
  figure, axes_array = plt.subplots(num_subplots, sharex=True)
  
  for key in data.keys():
    # grab the data values for this series
    y = data[key]
  
    # we have no x-axis reference, so 
    #  we will simply plot each value incrementally
    #  along the x-axis, starting at 0, going up
    #  to len(y)
    x = range(len(y))
  
    # Now we need to use the config to plot
    #  this data on the correct subplot/axes
    # go through each item/plot in the config list
    for i in range(len(config)):
      if key in config[i]:
        # if this series belongs in this plot
        #  then plot it on the right axes
        axes_array[i].plot(x, y, label=key)
  
  initializeAxes()

  # Display
  plt.show()




# We process the config to initialize the plots
# config contains 1 item for each intended subplot.
#  the config is a list of list of metric-names:
#  (
#    ('x', 'y', 'z'),       # for subplot 0
#    ('r', 'n')             # for subplot 1
#  )
#  the top level list corresponds to subplots
#   each sub list contains the names of each metric that should be plotted in that subplot
def processConfig(config):
  #  The length of config should tell us how many subplots we want
  num_subplots = len(config)

  # Create a figure with several subplots
  #  number of subplots according to the config
  #  all subplots share the temporal axis (x)
  global figure
  global axes_array
  figure, axes_array = plt.subplots(num_subplots, sharex=True)

  # Now we ned to initialize each line
  # Iterate over each subplot config
  for subplot in range(len(config)):
    # intialize a dict for this subplot
    #  (the dict will be a metric->line mapping)
    lines.append(dict())

    # and iterate over each metric within
    for metric in config[subplot]:
      # plot an empty line to initialize, labeled with the metric name
      line, = axes_array[subplot].plot([], [], label=metric)
      # hold on to the line reference so that we can update the data 
      #  later when animating
      lines[subplot][metric] = line

  initializeAxes()





def initializeAxes():
  for axes in axes_array:
    axes.legend()
    axes.get_yaxis().get_major_formatter().set_useOffset(False)  


def updateAxes(frameNumber):
  for axes in axes_array:
    axes.relim()
    axes.autoscale_view(False, False, True)
    axes.set_xlim(frameNumber - viewSize, frameNumber)

# Update the lines based on the new data
def updateLines():  
  # Iterate over each metric (named series)
  for metric in data.keys():
    # grab the data values for this series
    y = data[metric]

    # we have no x-axis reference, so 
    #  we will simply plot each value incrementally
    #  along the x-axis, starting at 0, going up
    #  to len(y)
    x = range(len(y))

    # Find the correct lines to update
    for subplot in range(len(lines)):
      if metric in lines[subplot]:
        # set the new data
        lines[subplot][metric].set_data(x, y)

def update(frameNumber, serialInput):
  debug("Update %s", (frameNumber))
  line = serialInput.readline().decode("utf-8")
  processLine(line)
  updateLines()
  updateAxes(frameNumber)

