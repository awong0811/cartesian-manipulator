const int switchPin = 2; // Pin connected to the NO switch
const char outputChar = 'A'; // Character to output when switch is pressed

void setup() {
  pinMode(switchPin, INPUT_PULLUP); // Set the switch pin as an INPUT
  Serial.begin(9600); // Start the Serial communication at 9600 baud
}

void loop() {
  // Read the state of the switch
  int switchState = digitalRead(switchPin);
  
  // Check if the switch is pressed
  if (switchState == LOW) {
    Serial.println(outputChar); // Output the character to Serial Monitor
    delay(100); // Delay to avoid multiple readings from one press
  }
}
