// Define the pins connected to your 5 LEDs
const int ledPins[5] = {2, 3, 4, 5, 6}; 

void setup() {
  // Initialize all 5 pins as outputs and turn them off
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
  // Start Serial communication at 9600 baud rate
  Serial.begin(9600); 
}

void loop() {
  // Wait until Python sends exactly 5 data bytes (one for each finger)
  if (Serial.available() >= 5) {
    for (int i = 0; i < 5; i++) {
      char state = Serial.read(); // Read '1' or '0' for the current finger
      
      if (state == '1') {
        digitalWrite(ledPins[i], HIGH); // Turn LED On
      } else if (state == '0') {
        digitalWrite(ledPins[i], LOW);  // Turn LED Off
      }
    }
    
    // Flush out any extra character remnants to prevent data desync
    while(Serial.available() > 0) {
      Serial.read();
    }
  }
}