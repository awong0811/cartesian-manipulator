from src.arduino import Arduino
import time

instrument = Arduino(port='COM16')
instrument.connect()

instrument.send_command(command='X1?')
time.sleep(0.5)
response = instrument.read_response()
print(response)
instrument.send_command(command='X2?')
time.sleep(0.5)
response = instrument.read_response()
print(response)

instrument.reset([1])
instrument.reset([2])
instrument.get_coords()
# for i in range(10):
#     instrument.move([1],[1000])
#     instrument.move([2],[1000])

instrument.disconnect()