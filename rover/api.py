
from django.http import JsonResponse
from . import arm_controller

def control(request):
	command = request.GET.get('command')
	status = arm_controller.control(command)
	return JsonResponse({"success": status})


# claw releases item into bin, when released send data to dashboard 


def test(request):
	return JsonResponse({"message": 'You have successfully connected to the Pi API'})