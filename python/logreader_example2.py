#!/usr/bin/python3
# test logreader
from logreader import LogReader
import os

### Example 2 ########################################################
# Now an example, reading from a file 
#  The file we'll use is ./examples/1.data
# First we need to get the path of the file we're reading from 
current_directory = os.path.dirname(__file__) #<-- absolute dir the script is in
relative_path_to_data_file = "example/1.data"
file_path = os.path.join(current_directory, relative_path_to_data_file)

l = LogReader()
l.readFile(file_path)

# Now let's see the series of data we have for each metric
for metric in l.getData():
  print("%s: %s" % (metric, l.getData()[metric]))
