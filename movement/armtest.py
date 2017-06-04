from __future__ import division
import time
import Adafruit_PCA9685
import RPiArm

if __name__ == "__main__":
    arm = RPiArm.RPiArm()

    # ticks = servo_reset
    # servo_move = 15

    while(1):
        print("\n")
        print("Enter command: ")
        command = raw_input()

        if command == "open":
            arm.move_claw("open")

        elif command == "close":
            arm.move_claw("close")

        elif command == "rotate claw L":
            arm.rotate_claw("left")

        elif command == "rotate claw R":
            arm.rotate_claw("right")

        elif command == "rotate claw C":
            arm.rotate_claw("center")

        elif command == "rotate base L":
            arm.rotate_base("left")

        elif command == "rotate base R":
            arm.rotate_base("right")

        elif command == "rotate base C":
            arm.rotate_base("center")

        elif command == "move3 B":
            arm.move_servo3("backward")

        elif command == "move3 F":
            arm.move_servo3("forward")

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
