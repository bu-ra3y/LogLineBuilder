#!/usr/bin/python3
# test logreader
import logreader

logreader.readInput('test/1.data')
d = logreader.getData()

# print out the names of the series we have
print(d.keys())

# print out all the data
print(d)

# divide up the series into 2 plots:
#   first: z, y, m, x, dist
#   second: pan, tilt
config=[['z','y','m','x','dist'], ['pan','tilt']]

# plot it!
logreader.plotData(config)