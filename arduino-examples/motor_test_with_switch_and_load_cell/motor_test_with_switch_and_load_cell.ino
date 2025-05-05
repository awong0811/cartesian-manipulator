// Script to test motor control of all motors over serial
// 2024-03-12
//
// NDE URAs ->
// Joshua Taylor
// Jimmy Huang
// Anthony Wong

#include <Servo.h>
#include <AccelStepper.h>
#include <HX711_ADC.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

//
// CONSTANT DEFINITIONS
//
#define SERIAL_STALL 10  //ms

//
// PIN NUMBERS
//
#define X1_PUL 2
#define X1_DIR 3

#define X2_PUL 8
#define X2_DIR 9

#define Y_PUL 5
#define Y_DIR 4

#define Z_PUL 10
#define Z_DIR 11

const int HX711_dout = 32;  //mcu > HX711 dout pin
const int HX711_sck = 30;   //mcu > HX711 sck pin



//
// DRIVER OBJECTS
//
// Define a stepper and the pins it will use
// 1 or AccelStepper::DRIVER means a stepper driver (with Step and Direction pins)
AccelStepper x1_stepper(AccelStepper::DRIVER, X1_PUL, X1_DIR);
AccelStepper x2_stepper(AccelStepper::DRIVER, X2_PUL, X2_DIR);
AccelStepper y_stepper(AccelStepper::DRIVER, Y_PUL, Y_DIR);
AccelStepper z_stepper(AccelStepper::DRIVER, Z_PUL, Z_DIR);
Servo myServo;

//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);

//
// GLOBAL MESSGAGE VARIABLES
//
char CMD;
long PARAM1;
float i = 0;
const int switchPin1 = 23;          // Pin connected to the NO switch, switch 1, for motor x1
const String outputSwitch1 = "S1";  // Character to output when switch 1 is pressed
const int switchPin2 = 43;          // Switch 2, for motor x2
const String outputSwitch2 = "S2";
const int switchPin3 = 31;  // Switch 3, for motor y
const String outputSwitch3 = "S3";
const int switchPin4 = 39;  // Switch 4, for motor z
const String outputSwitch4 = "S4";

const int calVal_eepromAdress = 0;
unsigned long t = 0;
bool calibrated = false;
bool moved = false;
unsigned long previousMillis = 0;  // Last time data was updated
const long interval = 1000;        // 1 second (1000 milliseconds)

void setup() {
  // Set the control input rate
  Serial.begin(9600);

  // Set each of the switch pins to input with inbuilt pullup resistor
  pinMode(switchPin1, INPUT_PULLUP);
  pinMode(switchPin2, INPUT_PULLUP);
  pinMode(switchPin3, INPUT_PULLUP);
  pinMode(switchPin4, INPUT_PULLUP);

  myServo.attach(7);
  myServo.write(0);

  // Set the speeds for each motor
  x1_stepper.setMaxSpeed(500.0);
  // x1_stepper.setSpeed(2500.0);
  x1_stepper.setAcceleration(1000.0);
  x2_stepper.setMaxSpeed(500.0);
  // x2_stepper.setSpeed(250000.0);
  x2_stepper.setAcceleration(1000.0);
  y_stepper.setMaxSpeed(500.0);
  // y_stepper.setSpeed(250000.0);
  y_stepper.setAcceleration(1000.0);
  z_stepper.setMaxSpeed(1000.0);
  z_stepper.setAcceleration(1000.0);

  LoadCell.begin();
  //LoadCell.setReverseOutput(); //uncomment to turn a negative output value to positive
  unsigned long stabilizingtime = 2000;  // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = true;                  //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1)
      ;
  } else {
    LoadCell.setCalFactor(1.0);  // user set calibration value (float), initial value 1.0 may be used for this sketch
    Serial.println("Startup is complete");
  }
  LoadCell.setSamplesInUse(100);
}

void loop() {
  // This actually moves the stepper motor
  while (calibrated == false) {
    Serial.println("***");
    Serial.println("Start calibration:");
    Serial.println("Remove any load applied to the load cell.");
    Serial.println("Send 't' from serial monitor to set the tare offset or 's' to skip the setup phase.");

    boolean _resume = false;
    while (_resume == false) {
      LoadCell.update();
      if (Serial.available() > 0) {
        if (Serial.available() > 0) {
          char inByte = Serial.read();
          if (inByte == 't') LoadCell.tareNoDelay();
          if (inByte == 's'){
            Serial.println("Setup phase skipped.");
            _resume = true;
            calibrated = true;
          }
        }
      }
      if (LoadCell.getTareStatus() == true) {
        Serial.println("Tare complete");
        _resume = true;
      }
    }
    if (calibrated) //skip setup phase
      break;

    Serial.println("Now, move the transducer to the scale until a suitable weight is measured. Type 'd' when done.");


    while (moved == false) {
      z_stepper.run();
      if (Serial.available()) {
        char in = Serial.read();

        // Check for Z-axis movement command
        if (in == 'Z') {
          // Wait for the next byte and get the command
          if (getCommand()) {
            if (CMD == '?')  // Query position of Z-axis
            {
              Serial.print("Z@");
              Serial.print(z_stepper.currentPosition());
              Serial.print('\n');
            } else if (CMD == ':')  // Move to absolute position
            {
              z_stepper.moveTo(PARAM1);
            } else if (CMD == '+')  // Move up by PARAM1
            {
              z_stepper.move(PARAM1);
            } else if (CMD == '-')  // Move down by PARAM1
            {
              z_stepper.move(PARAM1);
            }
          }
        } else if (in == 'd') {
          moved = true;
        }
      }
    }

    Serial.println("Then send the weight of this weight (i.e. 100.0) from serial monitor.");
    float known_mass = 0;
    _resume = false;
    while (_resume == false) {
      LoadCell.update();
      if (Serial.available() > 0) {
        known_mass = Serial.parseFloat();
        if (known_mass != 0) {
          Serial.print("Known mass is: ");
          Serial.println(known_mass);
          _resume = true;
        }
      }
    }
    LoadCell.refreshDataSet();                                           //refresh the dataset to be sure that the known mass is measured correct
    float newCalibrationValue = LoadCell.getNewCalibration(known_mass);  //get the new calibration value
    LoadCell.setCalFactor(newCalibrationValue);
    Serial.print("New calibration value has been set to: ");
    Serial.println(newCalibrationValue);
    Serial.println("Setup complete!");
    calibrated = true;
  }
  static boolean newDataReady = 0;

  // check for new data/start next conversion:
  if (LoadCell.update()) newDataReady = true;

  if (millis() - previousMillis >= interval) {  // If 1 second has passed
    previousMillis = millis();                  // Save the current time

    // Update the load cell and get the new data
    if (LoadCell.update()) {
      newDataReady = true;
    }

    // Get smoothed value from the dataset:
    if (newDataReady) {
      i = LoadCell.getData();
      newDataReady = 0;
    }
  }

  x1_stepper.run();
  x2_stepper.run();
  y_stepper.run();
  z_stepper.run();

  //////////////////// SWITCHES
  // Read the state of the switch
  int switchState1 = digitalRead(switchPin1);
  int switchState2 = digitalRead(switchPin2);
  int switchState3 = digitalRead(switchPin3);
  int switchState4 = digitalRead(switchPin4);
  // Check if the motor is moving forward or backward (only stop the motor if it is moving forward into the switch)
  if (x1_stepper.distanceToGo() > 0) {
    if (switchState1 == LOW) {
      Serial.println(outputSwitch1);  // Output the character to Serial Monitor
      x1_stepper.setCurrentPosition(x1_stepper.currentPosition());
      x1_stepper.stop();
    }
  }
  if (x2_stepper.distanceToGo() > 0) {
    if (switchState2 == LOW) {
      Serial.println(outputSwitch2);  // Output the character to Serial Monitor
      x2_stepper.setCurrentPosition(x2_stepper.currentPosition());
      x2_stepper.stop();
    }
  }
  if (y_stepper.distanceToGo() > 0) {
    if (switchState3 == LOW) {
      Serial.println(outputSwitch3);  // Output the character to Serial Monitor
      y_stepper.setCurrentPosition(y_stepper.currentPosition());
      y_stepper.stop();
    }
  }
  if (z_stepper.distanceToGo() < 0) {
    if (switchState4 == LOW) {
      Serial.println(outputSwitch4);  // Output the character to Serial Monitor
      z_stepper.setCurrentPosition(z_stepper.currentPosition());
      z_stepper.stop();
    }
  }
  //////////////////////////////
  // Check if we have a message from the PC
  if (Serial.available()) {
    char in = Serial.read();
    // get load cell output
    if (in == 'l') {
      Serial.print("Load_cell output val: ");
      Serial.println(i);
    }

    // moveTo command sets the target, then waits for the run command to do the steps
    // Move z-axis up or down
    if (in == 'Z') {
      // Wait for next byte
      // Get command
      if (getCommand()) {
        if (CMD == '?')  // Query position
        {
          Serial.print("Z@");
          Serial.print(z_stepper.currentPosition());
          Serial.print('\n');
        } else if (CMD == ':')  // Move to absolute position
        {
          z_stepper.moveTo(PARAM1);
        } else if (CMD == '+')  // Move up by PARAM1
        {
          z_stepper.move(PARAM1);
        } else if (CMD == '-')  // Move down by PARAM1
        {
          z_stepper.move(PARAM1);
        }
      }
    }

    // Move any other axis on the system
    else if (in == 'X') {
      // Wait for next byte
      if (waitForSerial()) {
        in = Serial.read();

        // X1 selected
        if (in == '1') {
          // Get command
          if (getCommand()) {
            if (CMD == '?') {
              Serial.print("X1@");
              Serial.print(x1_stepper.currentPosition());
              Serial.print('\n');
            } else if (CMD == ':') {
              x1_stepper.moveTo(PARAM1);
            } else if (CMD == '+') {
              x1_stepper.move(PARAM1);
            } else if (CMD == '-') {
              x1_stepper.move(PARAM1);
            }
          }
        }
        // X2 selected
        else if (in == '2') {
          // Get command
          if (getCommand()) {
            if (CMD == '?') {
              Serial.print("X2@");
              Serial.print(x2_stepper.currentPosition());
              Serial.print('\n');
            } else if (CMD == ':') {
              x2_stepper.moveTo(PARAM1);
            } else if (CMD == '+') {
              x2_stepper.move(PARAM1);
            } else if (CMD == '-') {
              x2_stepper.move(PARAM1);
            }
          }
        }
      }
    } else if (in == 'Y') {
      // Get command
      if (getCommand()) {
        if (CMD == '?') {
          Serial.print("Y@");
          Serial.print(y_stepper.currentPosition());
          Serial.print('\n');
        } else if (CMD == ':') {
          y_stepper.moveTo(PARAM1);
        } else if (CMD == '+') {
          y_stepper.move(PARAM1);
        } else if (CMD == '-') {
          y_stepper.move(PARAM1);
        }
      }
    } else if (in == 'W') {
      
      myServo.write(180);
      delay(2000);
      x2_stepper.move(-100);  // Set the target move
      // Keep running the stepper until it reaches the target
      while (x2_stepper.distanceToGo() != 0) {
        x2_stepper.run();
      }
      myServo.write(0);
      x2_stepper.move(100);
      while (x2_stepper.distanceToGo() != 0) {
        x2_stepper.run();
      }
      // After the stepper is finished, move the servo instantly
      
      
    }
  }
}
// Wait for message from PC or timeout
bool waitForSerial() {
  unsigned long start = millis();

  // Stall for SERIAL_STALL milliseconds
  while (millis() - start < SERIAL_STALL && !Serial.available())
    ;

  return Serial.available();
}

// Get standard command from PC or timeout
bool getCommand() {
  // Wait for next byte
  if (waitForSerial()) {
    CMD = Serial.read();

    // Where query
    if (CMD == '?') {
      return true;
    }
    // Absolute position, relative position
    else if (CMD == ':' || CMD == '+' || CMD == '-') {
      char in = '\0';
      PARAM1 = 0;

      // Get the integer that follows
      while (waitForSerial()) {
        in = Serial.read();

        // End of message
        if (in == '\n' || in == ',') {
          break;
        }
        // Got a digit
        else if (in >= '0' && in <= '9') {
          PARAM1 *= 10;
          PARAM1 += (in - '0');
        }
        // Invalid character
        else {
          return false;
        }
      }

      // Make sure the message was successful
      if (in == '\n' || in == ',') {
        if (CMD == '-') {
          PARAM1 = -PARAM1;
        }
        return true;
      }
    }
  }

  return false;
}
