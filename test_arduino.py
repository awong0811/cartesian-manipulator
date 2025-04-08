from src.arduino import Arduino
import time

tolerance = 0.5
target = 50
kp, kd = 0.17, 1e-2

instrument = Arduino(port='COM16')
instrument.connect()
instrument.setup()
instrument.send_command(command='X1?')
time.sleep(0.5)
response = instrument.read_response()
print(response)
instrument.send_command(command='X2?')
time.sleep(0.5)
response = instrument.read_response()
print(response)

################################
# instrument.reset([1,2,3])
################################

print("Specify 5 coordinates, separated by spaces: ")
user_input = input()
user_coords = user_input.split()
user_coords = list(map(int, user_coords))
print(f"Number of coordinates received: {len(user_coords)}")

instrument.move(motor=[2],dist=[200])
instrument.moveTo(motor=[2], destination=[0])

for i in range(len(user_coords)):
    instrument.moveTo(motor=[2], destination=[user_coords[i]])
    instrument.move(motor=[4], dist=[-1000], override=True)
    # while True:
    #     load = instrument.send_command('l')
    prev_error = 0
    while True:
        load = instrument.get_load()
        error = load - target
        if error <= tolerance:
            break
        correction = error*kp + kd*(error-prev_error)
        instrument.move(motor=[4], dist=[correction])
        prev_error = error
    instrument.moveTo(motor=[4], destination=[0])

instrument.moveTo(motor=[2], destination=[0])


# instrument.move(motor=[2, 3], dist=[2000, 1000], override=True)
# instrument.move(motor=[1,2,3],dist=[2000,3000,-5000],override=True)
# instrument.move(motor=[1,2], dist=[2000,1000])
# instrument.move(motor=[1,2], dist=[1000,2000])
# instrument.move(motor=[3],dist=[5000],override=True)
# instrument.reset([1,2])
# for i in range(3):
#     instrument.move([1],[1000])
#     instrument.move([2],[1000])
instrument.get_coords()


instrument.disconnect()