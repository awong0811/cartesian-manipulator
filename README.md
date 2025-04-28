# UCLA NDE Lab Cartesian Manipulator Project
Anthony Wong, Jimmy Huang, Joshua Taylor, Tristan Leonetti

## Installation
To use the environment.yml file, make sure you have Anaconda installed. Using the Anaconda command prompt, run the following.

```bash
$ conda env create -f environment.yml
```

If you don't want to install Anaconda, please create a Python virtual environment by running the following.
```bash
$ python -m venv nde-pymeasure
```
Install the packages by running the following.
```bash
$ pip install -r requirements.txt
```

## How It Works

### test_oscilloscope.py
This executable file creates a simple GUI in the terminal so the programmer can test the oscilloscope wrapper.

### test_arduino.py
This executable file allows the user to test certain commands or a stream of commands that are sent to an Arduino.

### gui.py
This executable file opens up the pymeasure GUI where the user can run experiments. (Not finished, please don't use.)

### AGILENT54624A Wrapper
This non-executable file in the src folder houses all of the I/O functions required to interface with the Agilent 54624A oscilloscope in the lab. Both the test.py and gui.py executable files use these functions to establish a connection, send commands, set oscilloscope settings, read responses, and decode responses. The docstrings in the file explain in greater detail how each function works.

### arduino source file
This non-executable file in the src folder has the functions that control movement of the stepper motors. It works by sending a command through serial communication with the Arduino. It can also read the output from the Arduino through serial. 

[Demos of work  can be seen here](https://drive.google.com/drive/folders/1gAUa8mZplnqo2Qg4ZMjdgH7VDHPlifyz?usp=drive_link)
