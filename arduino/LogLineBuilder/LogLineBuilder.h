// LogLineBuilder.h
// 
//
#ifndef LogLineBuilder_h
#define LogLineBuilder_h

#include "Arduino.h"

class LogLineBuilder {
  public: 
  	LogLineBuilder();
  	void put(String key, String value);
  	String getLine();
  private:
  	String _s;
};

#endif