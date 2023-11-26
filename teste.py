import serial_con
import time

motors = serial_con.Motors('/dev/ttyS0', 115200)

motors.forward()
time.sleep(2)
motors.turn_left()
time.sleep(1)
motors.stop()
