import serial
import time
import struct

class Agilent54624A():
    def __init__(self, port, baudrate=9600, timeout=1):
        '''
        Initialize the communication port of the computer, baud rate of the connection, and timeout.
        '''
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def connect(self):
        '''
        Establish a connection between the computer and the oscilloscope.
        '''
        try: 
            self.connection = serial.Serial(self.port, baudrate=self.baudrate, timeout = self.timeout)
            print("Connected to instrument")
        except serial.SerialException as e:
            print("Failed to connect to instrument:", e)

    def disconnect(self):
        '''
        Close the connection between the computer and the oscilloscope.
        '''
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from instrument")

    def send_command(self, command: str):
        '''
        Sends a command by encoding the string command as bytes and appending a command terminator.
        '''
        if self.connection is not None:
            try:
                print(f'Sending command [{len(command)}]: {command}')
                self.connection.write(command.encode() + b';') #sends command plus ; byte to terminate the command
                return None
            except serial.SerialException as c:
                print("Error sending command:", c)
                return None

    def read_response(self):
        '''
        Reads the output of the oscilloscope. Output is a string of bytes.
        '''
        print('Reading response... 0 bytes read', end='\r')
        if self.connection is not None:
            try:
                last_byte = time.time()
                response = b''
                # While the time between the last outputted byte is less than 3 seconds, keep reading
                while time.time() - last_byte < 3.000:
                    current = self.connection.read_all()
                    if current != b'':
                        last_byte = time.time()
                        response += current
                        print(f'Reading response... {len(response)} bytes read', end='\r')

                # If the response is not empty...
                if response is not None:
                    # Checks if the first byte of the response is a semicolon (has an ASCII value of 59)
                    # strips the response of the semicolon
                    if response[0] == int(b';'[0]):
                        response = response[1:]
                    else:
                        print()
                        print()
                        print(response[0])
                        print(b';')
                        print(int(b';'[0]))
                    # Decodes the response into a string, removing any leading and trailing spaces
                    try:
                        response = response.decode().strip()
                    except:
                        pass
                    print()
                    return response
                else:
                    print()
                    print("No response received")
                    return None
            except serial.SerialException as r:
                print("Error reading response: ", r)
                return None

    def checkOperational(self):
        '''
        Sends an identity command to check if the oscilloscope is responding normally.
        '''
        self.send_command("*IDN?")
        self.read_response()
        return None

    def select_channel(self, channel: int):
        '''
        Sets the channel to a desired channel.
        '''
        self.send_command(f":WAV:SOUR CHAN{channel}")
        print(f"Channel {channel} selected")
        return None

    def set_waveform_type(self, type: str):
        '''
        Sets the waveform type to one of three types: 'WORD', 'BYTE', or 'ASCII'.
        '''
        command = ":WAV:FORM " + type
        self.send_command(command = command)
        print("Waveform data display type set to ", type)
        return None

    def retrieve_data(self):
        '''
        Retrieves the datapoints of the waveform.
        '''
        # Send a command to retrieve the bytes that represent the datapoints
        self.send_command(command = ":WAV:DATA?")
        wait = 5
        while wait > 0:
            print(f'[{wait}]  ', end='\r')
            wait -= 1
            time.sleep(1)
        print('[0]')
            
        # Read in the bytes
        response = self.read_response()
        print()
        try:
            # Process the bytes
            if response[0:1].decode() == '#':
                # Second byte tells you how many of the following bytes complete the header
                btr = int(response[1:2].decode())
                totalBytes = int(response[2:2+btr].decode())
                headerSize = 2 + btr

                # Get whole number bytes per point
                # TODO get point count
                bytesPerPoint = int(totalBytes / 2000)

                # TODO determine unpack endianness
                unpackStr = '<B'
                if bytesPerPoint == 2:
                    unpackStr = '<H'

                start = headerSize + 1

                output = []
                # TODO point count
                for _ in range(1999):
                    output.append(struct.unpack(unpackStr, response[start:start + bytesPerPoint])[0])
                    start += bytesPerPoint

                response = output
            else:
                print(response[0:1])
            
        except Exception as e:
            print("Invalid response received! Error:", e)

        print("Points:", len(response))
        try:
            return response
        except Exception as e:
            print("No response")
            return None