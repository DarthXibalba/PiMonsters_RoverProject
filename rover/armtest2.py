from __future__ import division
import time
import Adafruit_PCA9685
from . import RPiArm

def control():
    arm = RPiArm.RPiArm()
    arm.reset_all()

    # ticks = arm.servo6.get_position()
    # servo_move = 15

    while(1):
        print("\n")
        print("Enter command: ")
        command = raw_input()

        if command == "move claw":
            print("Enter position: ")
            claw_pos = raw_input()
            if claw_pos == "open":
                arm.move_claw("open")
            elif claw_pos == "close":
                arm.move_claw("close")

        elif command == "rotate claw":
            print("Enter direction: ")
            rotate_dir = raw_input()
            if rotate_dir == "l":
                arm.rotate_claw("left")
            elif rotate_dir == "r":
                arm.rotate_claw("right")
            elif rotate_dir == "c":
                arm.rotate_claw("center")

        elif command == "rotate base":
            print("Enter direction: ")
            rotate_dir = raw_input()
            if rotate_dir == "l":
                arm.rotate_base("left")
            elif rotate_dir == "r":
                arm.rotate_base("right")
            elif rotate_dir == "c":
                arm.rotate_base("center")

        elif command == "move 3":
            print("Enter direction: ")
            move_dir = raw_input()
            if move_dir == "f":
                arm.move_servo3("forward")
            elif move_dir == "b":
                arm.move_servo3("backward")

        elif command == "move 4":
            print("Enter direction: ")
            move_dir = raw_input()
            if move_dir == "f":
                arm.move_servo4("forward")
            elif move_dir == "b":
                arm.move_servo4("backward")

        elif command == "move 5":
            print("Enter direction: ")
            move_dir = raw_input()
            if move_dir == "f":
                arm.move_servo5("forward")
            elif move_dir == "b":
                arm.move_servo5("backward")

        elif command == "general":
            print("Enter servo number: ")
            servo_number = raw_input()
            print("Enter ticks: ")
            tick_number = raw_input()
            arm.general_move(int(servo_number), int(tick_number))

        elif command == "slow":
            print("Enter servo number: ")
            servo_number = raw_input()
            print("Enter ticks: ")
            tick_number = raw_input()
            arm.slow_move(int(servo_number), int(tick_number))

        elif command == "reset":
            arm.reset_all()

        elif command == "stand":
            arm.stand_up()

        elif command == "pick":
            arm.pick_up()

        elif command == "drop":
            print("Enter direction: ")
            drop_dir = raw_input()
            if drop_dir == "l":
                arm.drop_can("left")
            elif drop_dir == "r":
                arm.drop_can("right")
            elif drop_dir == "c":
                arm.drop_can("center")

        elif command == "print":
            print("Enter servo number: ")
            servo_number = raw_input()
            arm.print_ticks(int(servo_number))

        # elif command == "a":
        #     if ticks < 600:
        #         ticks = ticks + servo_move
        #         arm.general_move(6, ticks)
        #     elif ticks >= 600:
        #         arm.general_move(6, 600)
        #
        # elif command == "d":
        #     if ticks > 200:
        #         ticks = ticks - servo_move
        #         arm.general_move(6, ticks)
        #     elif ticks <= 200:
        #         arm.general_move(6, 200)
        #
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
