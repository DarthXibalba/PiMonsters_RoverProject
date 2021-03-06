from __future__ import division
import time
import Adafruit_PCA9685

servo_increment = 5

class RPiServo:
    def __init__(self, channel, minTicks, maxTicks, resetTicks, waitTime):
        self.channel = channel
        self.minTicks = minTicks
        self.maxTicks = maxTicks
        self.resetTicks = resetTicks
        self.waitTime = waitTime
        self.on = 0
        self.off = resetTicks - 50

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

    def move_servo(self, off):
        if off < self.minTicks:
            self.off = self.minTicks
        elif off > self.maxTicks:
            self.off = self.maxTicks
        else:
            self.off = off
        self.pwm.set_pwm(self.channel, self.on, self.off)

    def get_position(self):
        return self.off

    def gentle_move(self, newPos):
        if newPos < self.minTicks:
            newPos = self.minTicks
        elif newPos > self.maxTicks:
            newPos = self.maxTicks

        if newPos < self.off:
            while(self.off > newPos):
                self.off -= servo_increment
                self.pwm.set_pwm(self.channel, self.on, self.off)
                time.sleep(self.waitTime)
        elif newPos > self.off:
            while(self.off < newPos):
                self.off += servo_increment
                self.pwm.set_pwm(self.channel, self.on, self.off)
                time.sleep(self.waitTime)

    def reset_servo(self):
        self.gentle_move(self.resetTicks)
