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
#define encoderA 18
#define encoderB 17

//
// DRIVER OBJECTS
//
// Define a stepper and the pins it will use
// 1 or AccelStepper::DRIVER means a stepper driver (with Step and Direction pins)
AccelStepper x1_stepper(AccelStepper::DRIVER, X1_PUL, X1_DIR);

//
// GLOBAL MESSGAGE VARIABLES
//
char CMD;
long PARAM1;


void setup()
{
  // Set the control input rate
  Serial.begin(9600);

  // Set the speeds for each motor
  x1_stepper.setMaxSpeed(1000.0);
  x1_stepper.setAcceleration(500.0);
  pinMode(encoderA, INPUT);
  pinMode(encoderB, INPUT);
}

void loop()
{
  // This actually moves the stepper motor
  x1_stepper.run();

  // Print Encoder A signal
  // Serial.println(digitalRead(encoderA));

  // Check if we have a message from the PC
  if (Serial.available())
  {
    char in = Serial.read();

    if (in == '?')
    {
      Serial.print("X1@");
      Serial.print(x1_stepper.currentPosition());
      Serial.print('\n');
    }
    // moveTo command sets the target, then waits for the run command to do the steps

    // Move z-axis up or down
    else if (in == 'U')
    {
      if (getCommand())
      {
        if (CMD == ':')
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
      //x1_stepper.moveTo(5000);
    }
    else if (in == 'D')
    {
      x1_stepper.moveTo(0);
    }
    // Move any other axis on the system
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
