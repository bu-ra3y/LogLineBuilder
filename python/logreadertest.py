#!/usr/bin/python3
# test logreader
import logreader

strPort="/dev/cu.usbmodem1411"
configString=[['pan', 'tilt', 'range'],['freeRam']]

logreader.plotDataLiveFromSerial(strPort, configString)
