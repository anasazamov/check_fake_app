from django.urls import path
from check_app.views import check_device, check_limit

urlpatterns = [
    path('check-device', check_device),
    path('check-limit', check_limit)
]