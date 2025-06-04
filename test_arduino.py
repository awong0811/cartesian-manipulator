from src.arduino import Arduino
import time
from src.agilent54624A import Agilent54624A
from src.utils import *
import argparse

tolerance = 1
target = 50
kp, kd = 1/0.0425, 0
dip_station_coord = 2090
couplant_increment = 50
vertical_offset = 22000 # between load cell and plate

parser = argparse.ArgumentParser(description="Process two file paths.")
parser.add_argument("input_file", type=str, help="Path to the input file")
parser.add_argument("output_file", type=str, nargs='?', default=None, help="Path to the output file")

args = parser.parse_args()
user_coords = get_user_coordinates(args.input_file)
print(f"Number of coordinates received: {len(user_coords)}")
if args.output_file is None:
    output_file = args.input_file
else:
    output_file = args.output_file

############ Set up oscilloscope ####################
# oscilloscope = Agilent54624A(port='COM1')
# oscilloscope.connect()
# oscilloscope.checkOperational()
#####################################################

# Set up arduino
arduino = Arduino(port='COM7')
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

##############################################################################
# Measurement loop
##############################################################################
pos, weight = boundary_condition
initial_guess = round(pos+kp*(float(weight) - target)) - vertical_offset
dip_pos = None
plate_pos = None
for i in range(len(user_coords)):
    if dip_pos is None:
        dip_pos = initial_guess
    if plate_pos is None:
        plate_pos = initial_guess
    arduino.pump_couplant(amount=couplant_increment)
    dip_pos = arduino.dip(dip_station_coord, dip_pos, target, tolerance, kp, kd)
    arduino.moveTo(motor=[2], destination=[user_coords[i]])
    plate_pos = arduino.controller(plate_pos, target, tolerance, kp, kd)

    # Capture the datapoints from the transmitter and receiver from the oscilloscope
    # datapoints_tx = oscilloscope.collect_datapoints('tx')
    # datapoints_rx = oscilloscope.collect_datapoints('rx')
    # if i < 1:
    #     datapoints = np.vstack([np.array(datapoints_tx), np.array(datapoints_rx)])
    # else:
    #     datapoints = np.vstack([datapoints, np.array(datapoints_tx), np.array(datapoints_rx)])
    #################################################################################

    arduino.move(motor=[4], dist=[2000])
    arduino.wipe()
    arduino.moveTo(motor=[4], destination=[0])

arduino.moveTo(motor=[2], destination=[0])
arduino.get_coords()

################# uncomment if using oscilloscope ##############################################
# datapoints = datapoints.T
# columns = [f"{'TX' if i % 2 == 0 else 'RX'}{i // 2 + 1}" for i in range(datapoints.shape[1])]
# save_data(output_file, columns=columns, datapoints=datapoints)
# oscilloscope.disconnect()
################################################################################################

arduino.disconnect()