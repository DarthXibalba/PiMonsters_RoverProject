
from django.http import JsonResponse
from . import arm_controller

def control(request):
	arm_controller.control()
	return JsonResponse({"success": status})


# claw releases item into bin, when released send data to dashboard 


def test(request):
	return JsonResponse({"message": 'You have successfully connected to the Pi API'})