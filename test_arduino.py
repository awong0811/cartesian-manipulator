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

# instrument.send_command(command='X1-10000,X2-10000')
# time.sleep(10)

# dist = 9999
# instrument.send_command(command=f'X2-{dist}')
# time.sleep(wait_times[dist//1000+1])
dist = 4999
instrument.send_command(command=f'X2+{dist}')
time.sleep(wait_times[dist//1000+1])
instrument.send_command(command=f'X2+{dist}')
time.sleep(wait_times[dist//1000+1])

# dist = 20000
# instrument.send_command(command=f'X2+{dist}')
# time.sleep(15)
# dist = 19000
# instrument.send_command(command=f'X2-{dist}')
# time.sleep(15)

# 19000 is the max distance from the switch!!!

instrument.disconnect()