// LogLineBuilder.cpp
// 
//
#include "Arduino.h"
#include "LogLineBuilder.h"

String _s = "";

LogLineBuilder::LogLineBuilder(){}

void LogLineBuilder::put(String key, String value) {
  Serial.print(key);
  Serial.print(" ");
  Serial.print(value);
  Serial.print(", ");
}

String LogLineBuilder::getLine(){
  return _s; 
}
