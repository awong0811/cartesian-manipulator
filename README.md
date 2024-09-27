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

### AGILENT54624A Wrapper
This non-executable file in the src folder houses all of the I/O functions required to interface with the Agilent 54624A oscilloscope in the lab. Both the test.py and gui.py executable files use these functions to establish a connection, send commands, set oscilloscope settings, read responses, and decode responses. The docstrings in the file explain in greater detail how each function works.

### test.py
This executable file creates a simple GUI in the terminal so the programmer can test the oscilloscope wrapper.

### gui.py
This executable file opens up the pymeasure GUI where the user can run experiments.