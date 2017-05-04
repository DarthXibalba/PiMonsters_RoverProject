from __future__ import division
import time
import Adafruit_PCA9685

class RPiServo:
    def __init__(self, servo_min, servo_max, servo_freq):
        self.servo_min = servo_min
        self.servo_max = servo_max
        self.servo_freq = servo_freq
        self.pwm = Adafruit_PCA9685.PCA9685()

    def test_servos(self):
        self.pwm.set_pwm_freq(self.servo_freq)
        self.pwm.set_all_pwm(self.servo_min, self.servo_max)

if __name__ == "__main__":
    my_min = 150
    my_max = 600
    my_freq = 60

    my_pwm = RPiServo(my_min, my_max, my_freq)

    while(1):
        my_pwm.test_servos()
        time.sleep(5)
