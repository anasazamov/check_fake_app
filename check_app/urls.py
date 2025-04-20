from django.urls import path
from check_app.views import check_device

urlpatterns = [
    path('check-device', check_device)
]