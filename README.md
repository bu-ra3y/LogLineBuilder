# Logger
A set of tools for dealing with data logged from an Arduino.

My scenario is that I am collecting a bunch of data on my Arduino and I want a 
way of sending it somewhere without having to think about how to format the data 
in a way that can be interpretted on the other side (serialization and deserialization).

Additionally, I want to monitor that data over time, visually, in real time.

This repository includes
- LogLineBuilder - An Arduino library for forumlating log lines of metrics
- logreader - A Python library for parsing the log lines into named series
- metricmonitor - A Python library for charting the metrics over time


## LogLineBuilder

Serialize data into a String suitable for writing out as a log line to an output interface.
The data is expected to be metrics - a key and a value, e.g. "voltage" and "5.5".  
You throw a bunch of these metrics into the LogLineBuilder with the put(k, v) method.
You get the final String with the getLine() method.

```c++
// you have some data: numbers as ints, longs, Strings
int r = 12;
long t = millis();
String x = "12.1";
...

// Use LogLineBuilder to prep the data for printing out (e.g. to the Serial device)
LogLineBuilder builder = LogLineBuilder();  // Create a LogLineBuilder
builder.put("time", t);                 	// put in a metric-value pair
builder.put("radius", r);                 	// another one
builder.put("x", x);                    	// more
Serial.println(builder.getLine());          // get the line of all the data ready for logging

```

Check out the included example Arduino sketch. Arduino > File > Examples > LogLineBuilder > example

## logreader
A Python module for reading in log lines that report metrics, which look like:

```
  key1 val1, key2 val2, key3 val3
  time 20127837, temp 12.828, mem 1712, altitude 123.22, x 0.212, y 0.1222
```

Can read from a (file | Python list | serial device) that present log lines, 
  or a single line/String itself. 
   
Parses the lines into a structure useful for working with the metric series

```python
    [
      'temperature' -> [12, 13, 14, 15, ...],
      'pressure'    -> [0.1, 0.2, 0.3, 0.4, ...],
      'memory'      -> [1021, 1022, 1023, 1024, ...],
      ...
    ]
```



## metricmonitor
A Python mondule for charting the metrics read by logreader over time.

```python
```
