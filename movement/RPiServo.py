from __future__ import division
import time
import Adafruit_PCA9685

# class RPiServo:
#     def __init__(self, servo_min, servo_max, servo_freq):
#         self.servo_min = servo_min
#         self.servo_max = servo_max
#         self.servo_freq = servo_freq
#         self.pwm = Adafruit_PCA9685.PCA9685()
#
#     def test_servos(self):
#         self.pwm.set_pwm_freq(self.servo_freq)
#         self.pwm.set_pwm(self.servo_min, self.servo_max)
#
# if __name__ == "__main__":
#     my_min = 150
#     my_max = 600
#     my_freq = 60
#
#     my_servo = RPiServo(my_min, my_max, my_freq)
#
#     while(1):
#         my_servo.move_servo()
#         time.sleep(5)


class RPiServo:
    def __init__(self, channel):
        self.channel = channel
        self.pwm = Adafruit_PCA9685.PCA9685()

        def set_freq(self, servo_freq):
            self.pwm.set_pwm_freq(servo_freq)

        def open_claw(self, on = 0, off = 215):
            self.pwm.set_pwm(self.channel, on, off)

        def close_claw(self, on = 0, off = 415):
            self.pwm.set_pwm(self.channel, on, off)

        def move_servo(self, on = 0, off):
            self.pwm.set_pwm(self.channel, on, off)


if __name__ == "__main__":
    servo1 = RPiServo(0)
    servo2 = RPiServo(1)
    # servo3 = RPiServo(4)
    # servo4 = RPiServo(5)
    # servo5 = RPiServo(8)
    # servo6 = RPiServo(9)

    servo1.set_freq(60)
    servo_reset = 200
    ticks = servo_reset
    servo_move = 10

    while(1):
        print("\n")
        print("Enter command: ")
        command = raw_input()

        if command == "open":
            servo1.open_claw()

        elif command == "close":
            servo1.close_claw()

        elif command == "moveL":
            ticks = servo_reset + servo_move
            servo2.move_servo(ticks)

        elif command == "moveR":
            ticks = servo_reset - servo_move
            servo2.move_servo(ticks)

        elif command == "reset":
            servo2.move_servo(servo_reset)

        else:
            print("Invalid command!")
