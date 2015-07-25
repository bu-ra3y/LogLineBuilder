#!/usr/bin/python3
# test logreader
import logreader
import serial

# logreader.readInFile('test/1.data')
# d = logreader.getData()

# print out the names of the series we have
# print(d.keys())

# print out all the data
# print(d)

# divide up the series into 2 plots:
#   first: z, y, m, x, dist
#   second: pan, tilt
config=[['time'],['rand'],['x']]

strPort="/dev/cu.usbmodem1411"
logreader.readInSerial(strPort, 100)

# plot it!
logreader.plotData(config)