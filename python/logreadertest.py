#!/usr/bin/python3
# test logreader


import logreader

logreader.readInput('test/1.data')
d = logreader.getData()
print(d.keys())
