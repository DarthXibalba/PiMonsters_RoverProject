from __future__ import division
import time
import Adafruit_PCA9685


class RPiServo:
    def __init__(self, channel):
        self.channel = channel
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.on = 0

    def set_freq(self, servo_freq):
        self.pwm.set_pwm_freq(servo_freq)

    def open_claw(self):
        off = 125
        self.pwm.set_pwm(self.channel, self.on, off)

    def close_claw(self):
        off = 425
        self.pwm.set_pwm(self.channel, self.on, off)

    def move_servo(self, off):
        self.pwm.set_pwm(self.channel, self.on, off)


if __name__ == "__main__":
    servo1 = RPiServo(0)
    servo2 = RPiServo(1)
    # servo3 = RPiServo(4)
    # servo4 = RPiServo(5)
    # servo5 = RPiServo(8)
    # servo6 = RPiServo(9)

    servo1.set_freq(60)
    servo2.set_freq(60)
    servo_reset = 300
    ticks = servo_reset
    servo_move = 15
    servo_min = 150
    servo_max = 600

    while(1):
        print("\n")
        print("Enter command: ")
        command = raw_input()

        if command == "open":
            servo1.open_claw()

        elif command == "close":
            servo1.close_claw()

        elif command == "move1":
            ticks = ticks + servo_move
            servo2.move_servo(ticks)
            print ticks

        elif command == "move2":
            ticks = ticks - servo_move
            servo2.move_servo(ticks)
            print ticks

        elif command == "move3":
            servo2.move_servo(servo_min)

        elif command == "move4":
            servo2.move_servo(servo_min)

        elif command == "reset":
            servo2.move_servo(servo_reset)

        else:
            print("Invalid command!")
