
from django.http import JsonResponse
from . import armtest2, armmover

def control(request):
	status = armtest2.control()
	return JsonResponse({"success": status})


# claw releases item into bin, when released send data to dashboard 

def armmover(request):
	status = armtest2.move_arm()
	return JsonResponse({"success": status})

def test(request):
	return JsonResponse({"message": 'You have successfully connected to the Pi API'})