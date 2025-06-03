from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from check_app.models import Device, MTT, Token, PhoneDevice
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from check_app.admin import INTEGRITY_TOKEN, TokenAdmin
import logging
from django.core.exceptions import MultipleObjectsReturned
from django.contrib import admin
# from django.contrib.admin.sites import site
logger = logging.getLogger('loger')

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
    
@csrf_exempt
def check_token(request: HttpRequest) -> JsonResponse:
 
    if request.method == 'POST':
        license = request.POST.get('license')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(request.POST)
        if not (license and username and password):
            return JsonResponse({'status': False})
        # print(license)
        device = Device.objects.filter(license=license)
        if not device.exists():
            return JsonResponse({'status': False})

        try:
            mtt, _ = MTT.objects.get_or_create(username=username, password=password, device=device.first())
        except MultipleObjectsReturned:
            mtt = MTT.objects.filter(username=username, password=password, token__isnull=False).first()
            # print(mtt.device.license)
        
        token = Token.objects.filter(mtt=mtt).first()
        if token:
            return JsonResponse({'status': True, 'token': token.token})
        token_obj = TokenAdmin(Token, admin.site)
        phohe_info = token_obj.generate_android_device_info()
        token = token_obj.token_func_v3(
            username=username,
            password=password,
            app_version="1212",
            device_id=phohe_info['device_id'],
            device_model=phohe_info['device_model'],
            device_manafacture=phohe_info['device_manufacturer'],
            device_name=phohe_info['device_name']
        )
        # print(token)
        if not token:
            return JsonResponse({'status': False})
        try:
            token_obj_2 = Token.objects.get_or_create(
                mtt=mtt,
                token=token
            )
        except MultipleObjectsReturned:
            token_obj_2 = Token.objects.filter(mtt=mtt, token=token).first()

        PhoneDevice.objects.get_or_create(
            token=token_obj_2,
            model=phohe_info['device_model'],
            manafacturer=phohe_info['device_manufacturer'],
            device_id=phohe_info['device_id'],
            device_name=phohe_info['device_name']
        )

        if token:
            return JsonResponse({'status': True, 'token': token})

        return JsonResponse({'status': False})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def check_phone_device(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        token = request.POST.get('token')
        if not token:
            return JsonResponse({'error': 'Device ID is required'}, status=400)

        
        phone_device = PhoneDevice.objects.filter(token__token=token).first()

        if not phone_device:
            return JsonResponse({'status': False, 'error': 'Phone device not found'}, status=404)
        
        return JsonResponse({
            'status': True,
            'device_model': phone_device.model,
            'device_manufacturer': phone_device.manafacturer,
            'device_name': phone_device.device_name,
            'device_id': phone_device.device_id,
        }, status=200)
        
        

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def tokens_list(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        tokens_data = Token.objects.all().values(
            'token'
        )
        
        return JsonResponse(list(tokens_data), status=200, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=405)