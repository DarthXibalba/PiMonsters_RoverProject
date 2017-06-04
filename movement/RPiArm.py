from __future__ import division
import time
import Adafruit_PCA9685
import RPiServo


class RPiArm:
    def __init__(self):
        self.servo1 = RPiServo.RPiServo(0, 125, 525, 300)
        self.servo2 = RPiServo.RPiServo(1, 150, 600, 380)
        self.servo3 = RPiServo.RPiServo(4, 150, 600, 390)
        self.servo4 = RPiServo.RPiServo(5, 125, 600, 300)
        self.servo5 = RPiServo.RPiServo(8, 150, 600, 300)
        self.servo6 = RPiServo.RPiServo(9, 200, 600, 300)

    def move_claw(self, position):
        if position == "open":
            self.servo1.move_servo(125)
        elif position == "close":
            self.servo1.move_servo(525)

    def rotate_claw(self, position):
        if position == "left":
            self.servo2.move_servo(150)
        if position == "right":
            self.servo2.move_servo(600)
        if position == "center":
            self.servo2.move_servo(380)

    def move_servo3(self, position):
        if position == "forward":
            self.servo3.move_servo(600)
        elif position == "backward":
            self.servo3.move_servo(150)

    def move_servo4(self, position):
        if position == "forward":
            self.servo4.move_servo(600)
        elif position == "backward":
            self.servo4.move_servo(125)

    def move_servo5(self):
        self.servo5.move_servo(600)
        #forward = 150
        #backward = 600

    def rotate_base(self, position):
        if position == "left":
            self.servo6.move_servo(600)
        elif position == "right":
            self.servo6.move_servo(200)
        elif position == "center":
            self.servo6.move_servo(390)

    def general_move(self, servo_num, ticks):
        if servo_num == 1:
            self.servo1.move_servo(ticks)
        elif servo_num == 2:
            self.servo2.move_servo(ticks)
        elif servo_num == 3:
            self.servo3.move_servo(ticks)
        elif servo_num == 4:
            self.servo4.move_servo(ticks)
        elif servo_num == 5:
            self.servo5.move_servo(ticks)
        elif servo_num == 6:
            self.servo6.move_servo(ticks)

    def reset_all(self):
        self.servo2.move_servo(380)
        self.servo6.move_servo(390)

    def slow_move(self, servo_num, stopPos):
        if servo_num == 1:
            self.servo1.gentle_move(stopPos)
        elif servo_num == 2:
            self.servo2.gentle_move(stopPos)
        elif servo_num == 3:
            self.servo3.gentle_move(stopPos)
        elif servo_num == 4:
            self.servo4.gentle_move(stopPos)
        elif servo_num == 5:
            self.servo5.gentle_move(stopPos)
        elif servo_num == 6:
            self.servo6.gentle_move(stopPos)
