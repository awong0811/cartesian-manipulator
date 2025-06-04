from src.arduino import Arduino
import time

tolerance = 0.5
target = 50
kp, kd = 0.17, 1e-2

instrument = Arduino(port='COM7')
instrument.connect()
instrument.setup()
while True:
    user_input = input()
    if isinstance(user_input, str):
        try:
            if user_input == 'q':
                instrument.disconnect()
                exit()
            instrument.send_command(user_input)
        except ValueError:
            print("Not a valid input.")
    