# Logger
A tool for dealing with data logged from an Arduino

Includes
- LogLineBuilder - An Arduino library for forumlating log lines of metrics
- logreader - A Python library for parsing the log lines into named series


## LogLineBuilder
Serialize data into a String suitable for writing out as a log line to an output interface.
The data is expected to be metrics - a key and a value, e.g. "voltage" and "5.5".  
You throw a bunch of these metrics into the LogLineBuilder with the put(k, v) method.
You get the final String with the getLine() method.

```
LogLineBuilder builder = LogLineBuilder();      // Create a LogLineBuilder
builder.put("time", String(t));                 // put in a metric-value pair
builder.put("radius", String(r));                 // put in a metric-value pair
builder.put("x", String(x));                    // put in a metric-value pair
Serial.println(builder.getLine());              // get the line of all the data ready for logging

```
Check out the included exmaple Arduino sketch.


## logreader
A Python module for deserializing the log lines written by LogLineBuilder.
