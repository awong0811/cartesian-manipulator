// Script to test motor control of all motors over serial
// 2024-03-12
//
// NDE URAs ->
// Joshua Taylor
// Jimmy Huang
// Anthony Wong

#include <AccelStepper.h>

//
// CONSTANT DEFINITIONS
//
#define SERIAL_STALL 10 //ms

//
// PIN NUMBERS
//
#define X1_PUL 5
#define X1_DIR 6

#define X2_PUL 9
#define X2_DIR 10

#define Y_PUL 7
#define Y_DIR 8

#define Z_PUL 2
#define Z_DIR 3
#define Z_ENA 4


//
// DRIVER OBJECTS
//
// Define a stepper and the pins it will use
// 1 or AccelStepper::DRIVER means a stepper driver (with Step and Direction pins)
AccelStepper x1_stepper(AccelStepper::DRIVER, X1_PUL, X1_DIR);
AccelStepper x2_stepper(AccelStepper::DRIVER, X2_PUL, X2_DIR);
AccelStepper y_stepper(AccelStepper::DRIVER, Y_PUL, Y_DIR);
AccelStepper z_stepper(AccelStepper::DRIVER, Z_PUL, Z_DIR);

//
// GLOBAL MESSGAGE VARIABLES
//
char CMD;
long PARAM1;
const int switchPin1 = 22; // Pin connected to the NO switch, switch 1
const String outputSwitch1 = "S1"; // Character to output when switch 1 is pressed
const int switchPin2 = 23; // Switch 2
const String outputSwitch2 = "S2";
const int switchPin3 = 24;
const String outputSwitch3 = "S3";

void setup()
{
  // Set the control input rate
  Serial.begin(9600);

  // Never disable our Z axis for now (TODO)
  pinMode(Z_ENA, OUTPUT);
  digitalWrite(Z_ENA, LOW);

  // Set each of the switch pins to input with inbuilt pullup resistor
  pinMode(switchPin1, INPUT_PULLUP);
  pinMode(switchPin2, INPUT_PULLUP);
  pinMode(switchPin3, INPUT_PULLUP);

  // Set the speeds for each motor
  x1_stepper.setMaxSpeed(2500.0);
  // x1_stepper.setSpeed(2500.0);
  x1_stepper.setAcceleration(1000.0);
  x2_stepper.setMaxSpeed(2500.0);
  // x2_stepper.setSpeed(250000.0);
  x2_stepper.setAcceleration(1000.0);
  y_stepper.setMaxSpeed(2500.0);
  // y_stepper.setSpeed(250000.0);
  y_stepper.setAcceleration(1000.0);
  z_stepper.setMaxSpeed(2500.0);
  z_stepper.setAcceleration(500.0);
}

void loop()
{
  // This actually moves the stepper motor
  x1_stepper.run();
  x2_stepper.run();
  y_stepper.run();
  z_stepper.run();

  //////////////////// SWITCHES
  // Read the state of the switch
  int switchState1 = digitalRead(switchPin1);
  int switchState2 = digitalRead(switchPin2);
  int switchState3 = digitalRead(switchPin3);
  // Check if the motor is moving forward or backward (only stop the motor if it is moving forward into the switch)
  if (x1_stepper.distanceToGo()>0) {
    if (switchState1 == LOW) {
      Serial.println(outputSwitch1); // Output the character to Serial Monitor
      x1_stepper.setCurrentPosition(x1_stepper.currentPosition());
      x1_stepper.stop();
    }
  }
  if (x2_stepper.distanceToGo()>0) {
    if (switchState2 == LOW) {
      Serial.println(outputSwitch2); // Output the character to Serial Monitor
      x2_stepper.setCurrentPosition(x2_stepper.currentPosition());
      x2_stepper.stop();
    }
  }
  if (y_stepper.distanceToGo()<0) {
    if (switchState3 == LOW) {
      Serial.println(outputSwitch3); // Output the character to Serial Monitor
      y_stepper.setCurrentPosition(y_stepper.currentPosition());
      y_stepper.stop();
    }
  }
  //////////////////////////////
  
  // Check if we have a message from the PC
  if (Serial.available())
  {
    char in = Serial.read();
    
    // moveTo command sets the target, then waits for the run command to do the steps

    // Move z-axis up or down
    if (in == 'D')
    {
      z_stepper.moveTo(100);
    }
    else if (in == 'U')
    {
      z_stepper.moveTo(0);
    }
    // Move any other axis on the system
    else if (in == 'X')
    {
      // Wait for next byte
      if (waitForSerial())
      {
        in = Serial.read();

        // X1 selected
        if (in == '1')
        {
          // Get command
          if (getCommand())
          {
            if (CMD == '?')
            {
              Serial.print("X1@");
              Serial.print(x1_stepper.currentPosition());
              Serial.print('\n');
            }
            else if (CMD == ':')
            {
              x1_stepper.moveTo(PARAM1);
            }
            else if (CMD == '+')
            {
              x1_stepper.move(PARAM1);
            }
            else if (CMD == '-')
            {
              x1_stepper.move(PARAM1);
            }
          }
        }
        // X2 selected
        else if (in == '2')
        {
          // Get command
          if (getCommand())
          {
            if (CMD == '?')
            {
              Serial.print("X2@");
              Serial.print(x2_stepper.currentPosition());
              Serial.print('\n');
            }
            else if (CMD == ':')
            {
              x2_stepper.moveTo(PARAM1);
            }
            else if (CMD == '+')
            {
              x2_stepper.move(PARAM1);
            }
            else if (CMD == '-')
            {
              x2_stepper.move(PARAM1);
            }
          }
        }
      }
    }
    else if (in == 'Y')
    {
      // Get command
      if (getCommand())
      {
        if (CMD == '?')
        {
          Serial.print("Y@");
          Serial.print(y_stepper.currentPosition());
          Serial.print('\n');
        }
        else if (CMD == ':')
        {
          y_stepper.moveTo(PARAM1);
        }
        else if (CMD == '+')
        {
          y_stepper.move(PARAM1);
        }
        else if (CMD == '-')
        {
          y_stepper.move(PARAM1);
        }
      }
    }
  }
}

// Wait for message from PC or timeout
bool waitForSerial()
{
  unsigned long start = millis();

  // Stall for SERIAL_STALL milliseconds
  while (millis() - start < SERIAL_STALL && !Serial.available()) ;

  return Serial.available();
}

// Get standard command from PC or timeout
bool getCommand()
{
  // Wait for next byte
  if (waitForSerial())
  {
    CMD = Serial.read();

    // Where query
    if (CMD == '?')
    {
      return true;
    }
    // Absolute position, relative position
    else if (CMD == ':' || CMD == '+'  || CMD == '-')
    {
      char in = '\0';
      PARAM1 = 0;
      
      // Get the integer that follows
      while (waitForSerial())
      {
        in = Serial.read();

        // End of message
        if (in == '\n' || in == ',')
        {
          break;
        }
        // Got a digit
        else if (in >= '0' && in <= '9')
        {
          PARAM1 *= 10;
          PARAM1 += (in - '0');
        }
        // Invalid character
        else
        {
          return false;
        }
      }

      // Make sure the message was successful
      if (in == '\n' || in == ',')
      {
        if (CMD == '-')
        {
          PARAM1 = -PARAM1;
        }
        return true;
      }
    }
  }

  return false;
}
