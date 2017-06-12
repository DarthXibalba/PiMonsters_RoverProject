from __future__ import division
import time
import Adafruit_PCA9685
from . import RPiArm

def open_claw():
	arm = RPiArm.RPiArm()
	arm.move_claw("open")
	return True