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


# instrument.send_command(command='X1+1000')
# while True:
#     instrument.send_command(command='X1#')
#     time.sleep(0.1)
#     response = instrument.read_response()
#     if response and int(response[3:])==0:
#         break
#     time.sleep(1)
# instrument.send_command(command='X2+1000')
# while True:
#     instrument.send_command(command='X2#')
#     time.sleep(0.1)
#     response = instrument.read_response()
#     if response and int(response[3:])==0:
#         break
#     time.sleep(1)
instrument.send_command(command='X2-10000')
time.sleep(10)
# while True:
#     instrument.send_command(command='X2#')
#     time.sleep(1)
#     response = instrument.read_response()
#     print(int(response[3:]))
#     if response and int(response[3:])==0:
#         print("X1 has stopped")
#         break
#     time.sleep(1)
# instrument.send_command(command='X1-10000')
# while True:
#     instrument.send_command(command='X1#')
#     time.sleep(0.1)
#     response = instrument.read_response()
#     if response and int(response[3:])==0:
#         break
#     time.sleep(1)
# instrument.send_command(command='X1+10000,X2+10000')
# while True:
#     instrument.send_command(command='X1#')
#     time.sleep(0.1)
#     response1 = instrument.read_response()
#     instrument.send_command(command='X2#')
#     time.sleep(0.1)
#     response2 = instrument.read_response()
#     if response1 and response2 and response1[]==0 and response2==0:
#         break
#     time.sleep(1)
# instrument.send_command(command='X1-10000,X2-10000')
# while True:
#     instrument.send_command(command='X1#')
#     time.sleep(0.1)
#     response1 = instrument.read_response()
#     instrument.send_command(command='X2#')
#     time.sleep(0.1)
#     response2 = instrument.read_response()
#     if response1 and response2 and response1==0 and response2==0:
#         break
#     time.sleep(1)
instrument.disconnect()