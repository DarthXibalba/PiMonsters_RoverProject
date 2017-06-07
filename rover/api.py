
from django.http import JsonResponse
from . import arm_controller

def control(request):
	command = request.GET.get('command')
	status = arm_controller.control(command)
	return JsonResponse({"success": status})
