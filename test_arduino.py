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

wait_times = {
    1: 2.5,
    2: 3.5,
    3: 4,
    4: 4.5,
    5: 5,
    6: 5.5,
    7: 6,
    8: 6.5,
    9: 7,
    10: 7.5,
    11: 7.5
}


instrument.reset([1])
instrument.reset([2])
for i in range(10):
    instrument.move([1],[1000])
    instrument.move([2],[1000])


instrument.disconnect()