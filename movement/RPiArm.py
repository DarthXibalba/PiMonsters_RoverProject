from __future__ import division
import time
import Adafruit_PCA9685
import RPiServo


class RPiArm:
    def __init__(self):
        self.servo1 = RPiServo.RPiServo(0, 150, 600, 300)
        self.servo2 = RPiServo.RPiServo(1, 150, 600, 300)
        self.servo3 = RPiServo.RPiServo(4, 150, 600, 300)
        self.servo4 = RPiServo.RPiServo(5, 150, 600, 300)
        self.servo5 = RPiServo.RPiServo(8, 150, 600, 300)
        self.servo6 = RPiServo.RPiServo(9, 150, 600, 300)

    def open_claw(self):
        self.servo1.move_servo(125)
        # off = 125

    def close_claw(self):
        self.servo1.move_servo(500)
        # off = 425

    # def rotate_base(self):
    #     self.servo6.move_servo()
