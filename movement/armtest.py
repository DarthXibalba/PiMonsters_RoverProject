from __future__ import division
import time
import Adafruit_PCA9685
import RPiArm

if __name__ == "__main__":
    arm = RPiArm.RPiArm()
    arm.reset_all()

    ticks = arm.servo6.get_position()
    servo_move = 15

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

        elif command == "move3 F":
            arm.move_servo3("forward")

        elif command == "move3 B":
            arm.move_servo3("backward")

        elif command == "move4 F":
            arm.move_servo4("forward")

        elif command == "move4 B":
            arm.move_servo4("backward")

        elif command == "move5 F":
            arm.move_servo5("forward")

        elif command == "move5 B":
            arm.move_servo5("backward")

        elif command == "general":
            print("Enter servo number: ")
            servo_number = raw_input()
            print("Enter ticks: ")
            tick_number = raw_input()
            arm.general_move(int(servo_number), int(tick_number))

        elif command == "a":
            if ticks < 600:
                ticks = ticks + servo_move
                arm.general_move(6, ticks)
            elif ticks >= 600:
                arm.general_move(6, 600)

        elif command == "d":
            if ticks > 200:
                ticks = ticks - servo_move
                arm.general_move(6, ticks)
            elif ticks <= 200:
                arm.general_move(6, 200)

        elif command == "slow":
            print("Enter servo number: ")
            servo_number = raw_input()
            print("Enter ticks: ")
            tick_number = raw_input()
            arm.slow_move(int(servo_number), int(tick_number))

        elif command == "reset":
            arm.reset_all()

        elif command == "print":
            print("Enter servo number: ")
            servo_number = raw_input()
            arm.print_ticks(servo_number)

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
