import serial
import time
import config
from typing import List

class Arduino():
    def __init__(self, port, baudrate=9600, timeout=1):
        '''
        Initialize the communication port of the computer, baud rate of the connection, and timeout.
        '''
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        for i in range(4):
            setattr(self, f'motor{i+1}', 0)

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
        Reads the serial output and returns it. Arduino may output multiple lines.
        '''
        lines = []
        if self.connection is not None:
            while self.connection.in_waiting > 0:
                time.sleep(0.1)
                # data = self.connection.readline().decode('utf-8').strip()  # Read and decode the data
                data = self.connection.read(self.connection.in_waiting).decode('utf-8')  # Read all available data
                lines = lines+data.splitlines()  # Split into individual lines
        return lines if len(lines)>0 else None

    def check_switch(self, response):
        '''
        Checks if the response is a switch press.
        '''
        if response and len(response)==2 and response[0]=='S' and response[1].isnumeric():
            return True, int(response[1])
        else:
            return False, 0
    
    def reset(self, motor: List):
        assert(len(motor)<=4)
        assert(max(motor)<=4)
        assert(min(motor)>=0)

        ### RESET ALL MOTORS AT ONCE ###
        command = ""
        for x in motor:
            name = config.MOTOR_NAME[x]
            if x == 3:
                command = command + ',' + name + f'-19000'
            else:
                command = command + ',' + name + f'+19000'
        self.send_command(command=command[1:])
        count = 0
        while True:
            response = self.read_response()
            if response:
                for x in response:
                    print(x)
                count += len(response)
                if count == len(motor):
                    break
        ################################


        ### RESET EACH MOTOR ONE BY ONE ###
        # for x in motor:
        #     motor_name = config.MOTOR_NAME[x]
        #     command = motor_name+'+19000'
        #     self.send_command(command=command)
        #     while True:
        #         response = self.read_response()
        #         if response:
        #             for x in response:
        #                 print(x)
        #             break
        ###################################
        print("All motors reset!")
        return None


    def move(self, motor: List, dist: List, override=False):
        command = ''
        assert(len(motor)==len(dist))
        assert(len(motor)<=4)
        assert(max(motor)<=4)
        assert(max([abs(x) for x in dist])<=19000)
        for i in range(len(motor)):
            if motor[i] == 4:
                override = True
            distance = dist[i]
            # check position of motor
            pos = getattr(self, f'motor{motor[i]}')
            # if not override and 0<=pos<=config.max_distance:
            if not override and pos<=config.max_distance:
                destination = pos+distance
                if destination > 19000:
                    distance = 19000-pos
                    destination = 19000
                elif destination < 0:
                    distance = -pos
                    destination = 0
            if override:
                if motor[i]!=4:
                    destination = distance
                else:
                    setattr(self, 'motor4', pos+distance)
            # flip the sign in the command to the arduino
            if distance<0:
                if motor[i]==3:
                    sign='-'
                else:
                    sign = '+'
            else:
                if motor[i]==3:
                    sign='+'
                else:
                    sign = '-'
            command = command + ',' + config.MOTOR_NAME[motor[i]] + sign + f'{abs(distance)}'
            # command = command + f',X{motor[i]}'+sign+f'{abs(distance)}'
            # save the position of each motor
            if motor[i]!=4:
                setattr(self, f'motor{motor[i]}', destination)
        self.send_command(command=command[1:])
        # wait for all the motors for finish moving
        time.sleep(config.wait_times[max([abs(x) for x in dist])//1000+1])
        return dist
    
    def moveTo(self, motor: List, destination: List):
        coords = self.get_coords()
        dist = []
        for i,m in enumerate(motor):
            dist.append(destination[i] - coords[m-1])
        dist = self.move(motor=motor, dist=dist)
        return dist

    def get_load(self):
        self.send_command(command='l')
        time.sleep(0.5)
        response = self.read_response()[0]
        print(response)
        load = float(response[22:])
        return load

    def get_coords(self):
        coords = []
        print("Getting motor coordinates:")
        for i in range(4):
            coord = getattr(self, f'motor{i+1}')
            coords.append(coord)
            print(f"Motor {i+1}: {coord}")
        return coords
    
    def setup(self):
        time.sleep(5)
        response = self.read_response()
        for r in response:
            print(r)
        user_input = input()
        while user_input != 't':
            user_input = input()
        self.send_command(command=user_input)
        time.sleep(2)
        response = self.read_response()
        for r in response:
            print(r)
        while True:
            user_input = input()
            if user_input == 'd':
                self.send_command(command=user_input)
                break
            try:
                user_input = int(user_input)
            except ValueError:
                print("Not a valid integer.")
            self.move(motor=[4], dist=[user_input], override=True)
        time.sleep(2)
        response = self.read_response()
        for r in response:
            print(r)
        user_input = input() #weight measurement
        self.send_command(command=user_input)
        time.sleep(5)
        response = self.read_response()
        for r in response:
            print(r)
        pos = getattr(self, 'motor4')
        self.moveTo(motor=[4], destination=[0])
        return pos, user_input