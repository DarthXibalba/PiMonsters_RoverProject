from __future__ import division
import time
import Adafruit_PCA9685
import RPiArm

if __name__ == "__main__":
    arm = RPiArm.RPiArm()

    ticks = servo_reset
    servo_move = 15

    while(1):
        print("\n")
        print("Enter command: ")
        command = raw_input()

        if command == "open":
            arm.open_claw()

        elif command == "close":
            arm.close_claw()

        # elif command == "move1":
        #     ticks = ticks + servo_move
        #     servo2.move_servo(ticks)
        #     print ticks
        #
        # elif command == "move2":
        #     ticks = ticks - servo_move
        #     servo2.move_servo(ticks)
        #     print ticks
        #
        # elif command == "move3":
        #     servo2.move_servo(servo_min)
        #
        # elif command == "move4":
        #     servo2.move_servo(servo_max)
        #
        # elif command == "reset":
        #     servo2.move_servo(servo_reset)

        else:
            print("Invalid command!")
