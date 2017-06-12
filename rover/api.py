
from django.http import JsonResponse
from . import armtest2, simple_arm

# need to import vision stuff

def control(request):
	command = request.GET.get('command')
	if command == "start":
		# run vision script to start robot
		pass		
	elif command == "stop":
		pass
		# run vision script to stop robot
		
	return JsonResponse({"success": status})



def simple_arm_test(request):
	status = simple_arm.open_claw()
	return JsonResponse({"success": status})

def test(request):
	return JsonResponse({"message": 'You have successfully connected to the Pi API'})