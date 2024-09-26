import serial
import time
import struct

class Agilent54624A():
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def connect(self):
        try: 
            self.connection = serial.Serial(self.port, baudrate=self.baudrate, timeout = self.timeout)
            print("Connected to instrument")
        except serial.SerialException as e:
            print("Failed to connect to instrument:", e)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from instrument")

    def send_command(self, command: str):
        if self.connection is not None:
            try:
                print(f'Sending command [{len(command)}]: {command}')
                self.connection.write(command.encode() + b';') #sends command plus ; byte to terminate the command
                return None
            except serial.SerialException as c:
                print("Error sending command:", c)
                return None

    def read_response(self):
        print('Reading response... 0 bytes read', end='\r')
        if self.connection is not None:
            try:
                last_byte = time.time()
                response = b''
                while time.time() - last_byte < 3.000:
                    current = self.connection.read_all()
                    if current != b'':
                        last_byte = time.time()
                        response += current
                        print(f'Reading response... {len(response)} bytes read', end='\r')

                if response is not None:
                    if response[0] == int(b';'[0]):
                        response = response[1:]
                    else:
                        print()
                        print()
                        print(response[0])
                        print(b';')
                        print(int(b';'[0]))

                    try:
                        response = response.decode().strip()
                    except:
                        pass
                    print()
                    # print("Received response: ", response)
                    return response
                else:
                    print()
                    print("No response received")
                    return None
            except serial.SerialException as r:
                print("Error reading response: ", r)
                return None

    def checkOperational(self):
        self.send_command("*IDN?")
        self.read_response()
        return None

    def select_channel(self, channel: int):
        self.send_command(f":WAV:SOUR CHAN{channel}")
        print(f"Channel {channel} selected")
        return None

    def set_waveform_type(self, type: str):
        command = ":WAV:FORM " + type
        self.send_command(command = command)
        print("Waveform data display type set to ", type)
        return None

    def retrieve_data(self, type = 'WORD'):
        self.send_command(command = ":WAV:DATA?")
        wait = 5
        while wait > 0:
            print(f'[{wait}]  ', end='\r')
            wait -= 1
            time.sleep(1)
        print('[0]')
        # if type=="WORD":
        #     bytes_per_word = 2
        #     response = self.connection.read(4011)
        #     response = [response[i:i+bytes_per_word] for i in range(11, len(response), bytes_per_word)]
        #     output = []
        #     for x in response:
        #         output.append(struct.unpack('>e', x)[0])
        #         print(output[-1])
        #     #response = [struct.unpack('<f', x)[0] for x in response]
            
        #     response = output
        # elif type=="BYTE":
        #     bytes_per_word = 1
        #     response = self.connection.read(2000)
        #     response = [response[i:i+bytes_per_word] for i in range(0, len(response), bytes_per_word)]
            #response = [struct.unpack('<d', x)[0] for x in response]
            
        response = self.read_response()
        print()
        try:
            if response[0:1].decode() == '#':
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


        # print("Datapoints: ", response)
        print("Points:", len(response))
        # try:
        #     import matplotlib.pyplot as plt
        #     plt.plot(response)
        #     plt.show()
        #     return response
        # except Exception as e:
        #     print("Failed to plot:", e)
        #     return None
        try:
            return response
        except Exception as e:
            print("No response")
            return None