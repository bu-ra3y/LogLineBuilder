from metricmonitor import MetricMonitor

# Replace this with the path to your Arduino serial device
#  Find this in the Arduino IDE: Tools > Port > <devicePath>
device = "/dev/cu.usbmodem1411"

# If you load up your Arduino with the included LogLineBuilder example sketch
#  your Serial device will recieve 3 metrics: rand, x, and time
# Let's create 2 charts, first containing rand and x, second containing time
plotConfig = \
  [
    ['rand', 'x'],
    ['time']
  ]
m = MetricMonitor()
m.plotDataLiveFromSerial(device, plotConfig)