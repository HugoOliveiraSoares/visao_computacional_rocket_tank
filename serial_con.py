import serial
import time

class Motors():

    def __init__(self, location, vel):
        self.location = location
        self.vel = vel
        self.esp = serial.Serial(location, vel, timeout=1)
        time.sleep(0.5)
        self.esp.reset_input_buffer()
        if self.esp.isOpen():
            print("{} connected!".format(self.esp.port))

    def forward(self):
        self.esp.write(b'w')
        r = self.esp.readline()
        print(f'Serial {r}')

    def turn_left(self):
        self.esp.write(b'a')
        r = self.esp.readline()
        print(f'Serial {r}')

    def turn_rigth(self):
        self.esp.write(b'd')
        r = self.esp.readline()
        print(f'Serial {r}')

    def stop(self):
        self.esp.write(b's')
        r = self.esp.readline()
        print(f'Serial {r}')
