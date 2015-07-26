#!/usr/bin/python3
#
# metricmonitor module
# 
# < some documentation >
#
#
#
# In Case there's an animation problem
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
from logreader import LogReader

#  
#
class MetricMonitor:
 # LogReader that will read our parse our log lines
  reader = LogReader()

  # Access to the raw metric series
  data = None

  # This is where we keep track of the plot lines we're drawing
  lines = list()
  
  # and the set of axes
  axes_array = list()
  
  # The figure we are plotting to
  figure = None

  # How many ticks we want to be viewing on the x-axis
  viewSize = 200

  # If we dont recieve a configString that tells us 
  #  about which metrics we want to see on which plots, 
  #   we're going to let data come in and detect the metrics
  #    from the data.  
  updatesToSkip = 4

  # Are we debugging? (print stuff out)
  DEBUG = True

  def __init__(self):
    self.data = self.reader.getData()
  
  # A simple method to only print something if debugging
  def debug(self, message, argumentList):
    if(self.DEBUG):
      print(message % argumentList)

  # Plot the data, live, reading from a serial port
  def plotDataLiveFromSerial(self, pathToSerialDevice, plotConfig):
    with serial.Serial(pathToSerialDevice, 9600) as ser:
      self.processConfig(plotConfig)
      animation.FuncAnimation(self.figure, self.update, fargs=[ser])
      plt.show()

  # Chart the data using MatPlotLib
  def plotData(self, config):
    # config contains 1 item for each intended subplot.
    #  thus, the length of config should tell us how many subplots we want
    num_subplots = len(config)
    
    # Create a figure with several subplots
    #  number of subplots according to the config
    #  all subplots share the temporal axis (x)
    self.figure, self.axes_array = plt.subplots(num_subplots, sharex=True)
    
    for key in self.data.keys():
      # grab the data values for this series
      y = self.data[key]
    
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
    
    self.initializeAxes()

    # Display
    plt.show()

  # We process the config to initialize the plots
  # config contains 1 item for each intended subplot.
  #  the config is a list of list of metric-names:
  #  [
  #    ['x', 'y', 'z'],       # for subplot 0
  #    ['r', 'n']             # for subplot 1
  #  ]
  #  the top level list corresponds to subplots
  #   each sub list contains the names of each metric that should be plotted in that subplot
  def processConfig(self, config):
    # If we recieved an empty config, we want to be able to just put all
    #  metrics on one chart (we need 1 subplot)
    #  but we can't initialize the lines because we don't know how many there will be
    #  or what their metric names will be
    #  we will detect that as the data comes in
    if config == "":
      self.figure, axes = plt.subplots(1)
      self.axes_array = [axes]
    else: # assuming we have a legit config...
      #  The length of config should tell us how many subplots we want
      num_subplots = len(config)

      # Create a figure with several subplots
      #  number of subplots according to the config
      #  all subplots share the temporal axis (x)
      self.figure, self.axes_array = plt.subplots(num_subplots, sharex=True)

      # Now we need to initialize each line - one for each metric in each subplot config
      for subplot in range(len(config)):
        # intialize a dict for this subplot
        #  (the dict will be a metric->line mapping)
        self.lines.append(dict())

        # and iterate over each metric within 
        for metric in config[subplot]:
          self.initializeLine(subplot, metric)

      # And now, intialize the axes, based on the lines
      self.initializeAxes()

  # Set up the legends, formatters, etc.
  def initializeAxes(self):
    for axes in self.axes_array:
      axes.legend()
      axes.get_yaxis().get_major_formatter().set_useOffset(False)  

  # As we animate, we want to update the bounds of each chart
  def updateAxes(self, frameNumber):
    for axes in self.axes_array:
      axes.relim()
      axes.autoscale_view(False, False, True)
      axes.set_xlim(frameNumber - self.viewSize, frameNumber)

  # draw an empty line with the correct name
  #  Gets us ready for looping animation
  def initializeLine(self, subplot, metric):
    line, = self.axes_array[subplot].plot([], [], label=metric)
    # hold on to the line reference so that we can update the data 
    #  later when animating
    self.lines[subplot][metric] = line

  # Check out our data to see if we think we have enough to infer
  #  the metrics we are charting
  def stillWaitingForData(self):
    # Clearly we have no data..
    self.debug("data looks like: %s", [self.data])
    if self.data == None:
      self.debug("Still waiting for data. None so far.")
      return True

    # Check each metric to see how many points it has
    for metric in self.data:
      # If any metric has more than updatesToSkip points, 
      #  then let's say we're good to go
      if len(self.data[metric]) > self.updatesToSkip:
        return False

    # Otherwise, we keep waiting
    self.debug("Still waiting for data. Waiting for a metric to have" + \
      "at least %s values", [self.updatesToSkip])
    return True

  # Update the lines based on the new data
  def updateLines(self):  
    # If we haven't initialized the plot lines, 
    #   because we never recieved a plotConfig,
    #     then we need to handle that
    if len(self.lines) == 0:
      # If we don't have a config, we're going to wait just a bit
      #  to let some data come in and then we'll examine the data
      #  to detect the metrics
      if self.stillWaitingForData():
        return
      self.lines.append(dict())
      for metric in self.data:
        self.initializeLine(0, metric)
      self.initializeAxes()
      return

    for subplot in range(len(self.lines)):
      # if metric in self.lines[subplot]:
      for metric in self.lines[subplot]:
        # grab the data values for this series
        y = self.data[metric]

        # we have no x-axis reference, so 
        #  we will simply plot each value incrementally
        #  along the x-axis, starting at 0, going up
        #  to len(y)
        x = range(len(y))

        # set the new data
        self.lines[subplot][metric].set_data(x, y)




  def update(self, frameNumber, serialInput):
    self.debug("Update %s", (frameNumber))
    line = serialInput.readline().decode("utf-8")
    self.reader.readLine(line)
    self.updateLines()
    self.updateAxes(frameNumber)
