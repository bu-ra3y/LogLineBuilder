// ---------------------------------------------------------------------------
// Example LogLineBuilder library sketch
// ---------------------------------------------------------------------------

#include <LogLineBuilder.h>

void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results.
}

void loop() {
  long r = random();           // create some data...
  long t = millis();
  int x = 5;

  LogLineBuilder builder = LogLineBuilder();      // Create a LogLineBuilder
  builder.put("time", t);                 // put in a metric-value pair
  builder.put("rand", r);                 // put in a metric-value pair
  builder.put("x", x);                    // put in a metric-value pair
  Serial.println(builder.getLine());              // get the line of all the data ready for logging
  delay(300);                              // Wait before looping
}