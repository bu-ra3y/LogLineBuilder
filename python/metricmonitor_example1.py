from metricmonitor import MetricMonitor

# Replace this with the path to your Arduino serial device
#  Find this in the Arduino IDE: Tools > Port > <devicePath>
device = "/dev/cu.usbmodem1411"

# If you load up your Arduino with the included LogLineBuilder example sketch
#  your Serial device will recieve 3 metrics: rand, x, and time
# Let's not worry about specifying what we want to do with each metric and just
#  start plotting right away ---
plotConfig = ""
m = MetricMonitor()
m.plotDataLiveFromSerial(device, plotConfig)