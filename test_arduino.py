from src.arduino import Arduino
import time

instrument = Arduino(port='COM16')
instrument.connect()

instrument.setup()

# instrument.send_command(command='X1?')
# time.sleep(0.5)
# response = instrument.read_response()
# print(response)
# instrument.send_command(command='X2?')
# time.sleep(0.5)
# response = instrument.read_response()
# print(response)

# instrument.reset([1,2,3])
# instrument.move(motor=[2],dist=[200])
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