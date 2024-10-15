import serial
import time

class Arduino():
    def __init__(self, port, baudrate=9600, timeout=1):
        '''
        Initialize the communication port of the computer, baud rate of the connection, and timeout.
        '''
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def connect(self):
        '''
        Establish a connection between the computer and the Arduino.
        '''
        try: 
            self.connection = serial.Serial(self.port, baudrate=self.baudrate, timeout = self.timeout)
            print("Connected to instrument")
            time.sleep(1)
        except serial.SerialException as e:
            print("Failed to connect to instrument:", e)

    def disconnect(self):
        '''
        Close the connection between the computer and the Arduino.
        '''
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from instrument")

    def send_command(self, command: str):
        '''
        Sends a command by encoding the string command as bytes and appending a command terminator.
        Need to update....
        '''
        if self.connection is not None:
            try:
                print(f'Sending command [{len(command)}]: {command}')
                command = command + '\n'
                self.connection.write(command.encode()) #sends command
                return None
            except serial.SerialException as c:
                print("Error sending command:", c)
                return None
            
    def read_response(self):
        '''
        Reads the serial output and returns it.
        '''
        if self.connection is not None:
            if self.connection.in_waiting > 0:
                data = self.connection.readline().decode('utf-8').strip()  # Read and decode the data
                return data
        return None

    def check_switch(self):
        '''
        Checks if the response is a switch press.
        '''
        data = self.read_response()
        if len(data)==2 and data[0]=='S' and data[1].isnumeric():
            return True, int(data[1])
        else:
            return False, 0
        
    
