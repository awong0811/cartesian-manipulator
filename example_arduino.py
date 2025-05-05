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
arduino.setup()
arduino.send_command(command='X1?')
time.sleep(0.5)
response = arduino.read_response()
print(response)
arduino.send_command(command='X2?')
time.sleep(0.5)
response = arduino.read_response()
print(response)

# move -> relative
arduino.reset(motor=[2])
arduino.move(motor=[2], dist=[500])
arduino.move(motor=[4], dist=[500])
arduino.move(motor=[2, 4], dist=[-100, -100])
arduino.move(motor=[2, 4], dist=[200, 500])

# moveTo -> absolute
arduino.moveTo(motor=[2, 4], destination=[0,0])

arduino.get_coords()

# oscilloscope.disconnect()
arduino.disconnect()