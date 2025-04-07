const int switchPin = 8; // Pin connected to the NO switch
const String outputChar = "S1"; // Character to output when switch is pressed

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
    delay(5); // Delay to avoid multiple readings from one press
  }
}
