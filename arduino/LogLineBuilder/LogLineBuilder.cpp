// LogLineBuilder.cpp
// formulates log lines from key-value pairs of data like:
//    key1 val1, key2 val2, key3 val3
// 
#include "Arduino.h"
#include "LogLineBuilder.h"

String _s = "";

LogLineBuilder::LogLineBuilder(){}

void LogLineBuilder::put(String key, String value) {
  if (s.length() > 0) {
	// If there is already data in the string
  	// then first add a comma
  	_s += ", ";
  }
  // Now append "key value" to the string
  _s += key +" "+ value;
}

String LogLineBuilder::getLine(){
  // Return the string, ready for logging
  return _s; 
}
