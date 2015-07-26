// LogLineBuilder.cpp
// 
// Formulates log lines from key-value pairs of data like:
//    key1 val1, key2 val2, key3 val3
//    time 20127837, temp 12.828, mem 1712, altitude 123.22, x 0.212, y 0.1222
// 
// Instances are throw away, use one per log line
// 
//    Initialize a LogLineBuilder
//       LogLineBuilder builder = LogLineBuilder();
//
//    Add key-value pairs
//       builder.put("altitude", alt); 
//       builder.put("temp", temp); 
//       builder.put("pressure", p); 
//
//    Finally, get the resultant line and do something with it like printing it
//       builder.getLine();
//
// 
#include "Arduino.h"
#include "LogLineBuilder.h"

String _s = "";

LogLineBuilder::LogLineBuilder(){}

void LogLineBuilder::put(String key, long value) {
	put(key, String(value));
}

void LogLineBuilder::put(String key, int value) {
	put(key, String(value));
}

void LogLineBuilder::put(String key, String value) {
  if (_s.length() > 0) {
	// If there is already data in the string, e.g.
	//   "x 5"
  	// then first add a comma to separate from the incoming data
  	//   "x 5, "
  	_s += ", ";
  }
  // Now append "key value" to the string
  _s += key +" "+ value;
}

String LogLineBuilder::getLine(){
  // Return the line, ready for logging
  return _s; 
}
