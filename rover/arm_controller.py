from __future__ import division
import time
import Adafruit_PCA9685
from . import RPiArm

import requests

client = requests.session()
URL = "http://pi-monsters-dashboard.herokuapp.com/update-event"

# Retrieve the CSRF token first
client.get(URL)  # sets cookie
csrftoken = client.cookies['csrf']

def control(command):

    arm = RPiArm.RPiArm()
    arm.reset_all()

    # ticks = arm.servo6.get_position()
    # servo_move = 15

    if command == "open claw":  
        arm.move_claw("open")
    elif command == "close claw":
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


    elif command == "drop left":
        arm.drop_can("left")
        payload = {'event_id': '1', 'container': 'coke_cans', 'csrfmiddlewaretoken': csrftoken}
        r = requests.post(URL, data=payload)
    elif drop_dir == "drop right":
        arm.drop_can("right")
        payload = {'event_id': '1', 'container': 'sprite_cans', 'csrfmiddlewaretoken': csrftoken}
        r = requests.post(URL, data=payload)
    elif drop_dir == "drop center":
        payload = {'event_id': '1', 'container': 'pepsi_cans', 'csrfmiddlewaretoken': csrftoken}
        r = requests.post(URL, data=payload)
        arm.drop_can("center")


    elif command == "print":
        print("Enter servo number: ")
        servo_number = raw_input()
        arm.print_ticks(int(servo_number))

    else:
        print("Invalid command!")

    return True
