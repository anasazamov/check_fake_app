from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from check_app.models import Device, MTT
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy

# Create your views here.


@csrf_exempt
def check_device(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        license = request.POST.get('license')
        if not license:
            return JsonResponse({'error': 'License is required'}, status=400)

        try:
            device, created = Device.objects.get_or_create(license=license)
            return JsonResponse({'status': device.status, 'is_delete': device.is_delete}, status=200)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Device not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def check_limit(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        license = request.POST.get('license')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (license and username and password):
            return JsonResponse({'status': False})

        device = Device.objects.filter(license=license)
        if not device.exists():
            return JsonResponse({'status': False})
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        MTT.objects.get_or_create(username=username, password=password, device=device.first())

        count = MTT.objects.filter(device=device.first()).count()
        if count <= device.first().limit:
            return JsonResponse({'status': True})
        
        return JsonResponse({'status': False})