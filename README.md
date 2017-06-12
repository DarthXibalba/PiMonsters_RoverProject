# PiMonsters_RoverProject
Repo for the Pi Monsters final project in ECE 188 (Spring 2017)

# console cable
screen /dev/cu.usbserial 115200

# get ip address of Pi
hostname -I

# if above doesn't work
ifconfig

look for inet address under wlan0 

# python 2.7
source realenv/bin/activate

# python 3
source roverenv/bin/activate

# assuming ip address is 100.82.130.122, port will be 8000
./manage.py runserver 100.82.130.122:8000

# test the api and you will receive a successful message
http://100.82.130.122:8000/test