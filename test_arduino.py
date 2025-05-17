from src.arduino import Arduino
import time
from src.agilent54624A import Agilent54624A
from src.utils import *
import argparse

tolerance = 1
target = 50
kp, kd = 1/0.0425, 0
dip_station_coord = 2050

parser = argparse.ArgumentParser(description="Process two file paths.")
parser.add_argument("input_file", type=str, help="Path to the input file")
parser.add_argument("output_file", type=str, help="Path to the output file")

args = parser.parse_args()
user_coords = get_user_coordinates(args.input_file)
output_file = args.output_file

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

# Reset motors
arduino.reset([2])

# Enter user-specified coordinates

# print("Specify 5 coordinates, separated by spaces: ")
# user_input = input()
# user_coords = user_input.split()
# user_coords = list(map(int, user_coords))

print(f"Number of coordinates received: {len(user_coords)}")

##############################################################################
# Measurement loop
##############################################################################
pos, weight = boundary_condition
initial_guess = round(pos+kp*(float(weight) - target))
for i in range(len(user_coords)):
    arduino.dip(dip_station_coord, initial_guess, target, tolerance, kp, kd)
    arduino.moveTo(motor=[2], destination=[user_coords[i]])
    arduino.controller(initial_guess, target, tolerance, kp, kd)
    # datapoints_tx = oscilloscope.collect_datapoints('tx')
    # datapoints_rx = oscilloscope.collect_datapoints('rx')
    # datapoints = np.vstack([np.array(datapoints_tx), np.array(datapoints_rx)]).T
    # save_data(output_file, datapoints)
    arduino.move(motor=[4], dist=[2000])
    arduino.wipe()
    arduino.moveTo(motor=[4], destination=[0])

arduino.moveTo(motor=[2], destination=[0])
arduino.get_coords()

# oscilloscope.disconnect()
arduino.disconnect()