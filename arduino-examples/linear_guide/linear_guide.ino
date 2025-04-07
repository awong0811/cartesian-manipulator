#include <AccelStepper.h>

#define SERIAL_STALL 10  // ms

// PIN NUMBERS
#define X1_PUL 5
#define X1_DIR 6

AccelStepper x1_stepper(AccelStepper::DRIVER, X1_PUL, X1_DIR);

void setup() {
  Serial.begin(9600); // Initialize serial communication
  x1_stepper.setMaxSpeed(1000.0); // Set the maximum speed
  x1_stepper.setAcceleration(500.0); // Set the acceleration
}

void loop() {
  static bool moving = true;
  if (moving) {
    x1_stepper.moveTo(1000); // Set target position to 100
  } else {
    x1_stepper.moveTo(0); // Set target position to 0
  }

  // Call run() continuously to move the stepper
  if (x1_stepper.distanceToGo() == 0) {
    moving = !moving; // Toggle direction when target is reached
    delay(1000); // Pause before reversing
  }

  x1_stepper.run(); // Keep the motor running toward the target

  // Print current position periodically
  static unsigned long lastSerialTime = 0;
  if (millis() - lastSerialTime > SERIAL_STALL) {
    Serial.println(x1_stepper.currentPosition());
    lastSerialTime = millis();
  }
}
