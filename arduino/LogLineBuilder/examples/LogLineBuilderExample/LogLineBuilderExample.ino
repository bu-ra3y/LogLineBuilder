// ---------------------------------------------------------------------------
// Example LogLineBuilder library sketch
// ---------------------------------------------------------------------------

#include <LogLineBuilder.h>

void setup() {
  Serial.begin(9600); // Open serial monitor at 115200 baud to see ping results.
}

void loop() {
  int r = random();           // create some data...
  int t = millis();
  int x = 5;

  LogLineBuilder builder = LogLineBuilder();      // Create a LogLineBuilder
  builder.put("time", String(t));                 // put in a metric-value pair
  builder.put("rand", String(r));                 // put in a metric-value pair
  builder.put("x", String(x));                    // put in a metric-value pair
  Serial.println(builder.getLine());              // get the line of all the data ready for logging
  delay(1000);                              // Wait 1s for good measure
}