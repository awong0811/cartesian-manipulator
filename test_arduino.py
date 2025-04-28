from src.arduino import Arduino
import time
# from src.agilent54624A import Agilent54624A

tolerance = 0.5
target = 50
kp, kd = 1/0.169, 0

# Set up oscilloscope
# oscilloscope = Agilent54624A(port='COM1')
# oscilloscope.connect()
# oscilloscope.checkOperational()

# Set up arduino
arduino = Arduino(port='COM16')
arduino.connect()
boundary_condition = arduino.setup()
arduino.send_command(command='X1?')
time.sleep(0.5)
response = arduino.read_response()
print(response)
arduino.send_command(command='X2?')
time.sleep(0.5)
response = arduino.read_response()
print(response)

################################
# arduino.reset([1,2,3])
################################

print("Specify 5 coordinates, separated by spaces: ")
user_input = input()
user_coords = user_input.split()
user_coords = list(map(int, user_coords))
print(f"Number of coordinates received: {len(user_coords)}")

# arduino.move(motor=[2],dist=[200])
# arduino.moveTo(motor=[2], destination=[0])

##############################################################################
# Measurement loop
##############################################################################
pos, weight = boundary_condition
initial_guess = round(pos+kp*(float(weight) - target))
for i in range(len(user_coords)):
    arduino.moveTo(motor=[2], destination=[user_coords[i]])
    arduino.move(motor=[4], dist=[initial_guess], override=True)
    print(f'Initial load: {arduino.get_load()}')
    time.sleep(5)
    prev_error = None
    while True:
        load = arduino.get_load()
        error = load - target
        print(f'Load: {load}, Error: {error}')
        if abs(error) <= tolerance:
            print(f'Final load: {load}')
            time.sleep(3)
            break
        if prev_error is None:
            prev_error = error
        correction = error*kp + kd*(error-prev_error)
        print(f'Correction: {correction}')
        arduino.move(motor=[4], dist=[round(correction)], override=True)
        prev_error = error
        time.sleep(3)
    # oscilloscope.collect_datapoints('tx')
    # oscilloscope.collect_datapoints('rx')
    arduino.moveTo(motor=[4], destination=[0])

arduino.moveTo(motor=[2], destination=[0])


# arduino.move(motor=[2, 3], dist=[2000, 1000], override=True)
# arduino.move(motor=[1,2,3],dist=[2000,3000,-5000],override=True)
# arduino.move(motor=[1,2], dist=[2000,1000])
# arduino.move(motor=[1,2], dist=[1000,2000])
# arduino.move(motor=[3],dist=[5000],override=True)
# arduino.reset([1,2])
# for i in range(3):
#     arduino.move([1],[1000])
#     arduino.move([2],[1000])
arduino.get_coords()

# oscilloscope.disconnect()
arduino.disconnect()