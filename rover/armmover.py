from __future__ import division
import time
import Adafruit_PCA9685
from . import RPiArm

def move_arm():
	arm = RPiArm.RPiArm()
	# arm.reset_all()
	arm.move_claw("open")
	# arm.drop_can("center")

	return True