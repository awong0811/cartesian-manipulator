from src.arduino import Arduino
import time

tolerance = 0.5
target = 50
kp, kd = 0.17, 1e-2

instrument = Arduino(port='COM16')
instrument.connect()
instrument.setup()
while True:
    user_input = input()
    try:
        user_input = int(user_input)
    except ValueError:
        print("Not a valid integer.")
    instrument.move(motor=[4], dist=[user_input], override=True)