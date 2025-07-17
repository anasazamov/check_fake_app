from django.urls import path
from check_app.views import check_device, check_limit, check_phone_device, check_token, tokens_list, integrity_token, get_integrity_token

urlpatterns = [
    path('check-device', check_device),
    path('check-limit', check_limit),
    path('check-token', check_token),
    path('check-phone', check_phone_device),
    path('tokens-list', tokens_list),
    # path('integrity-token', integrity_token),
    path('integrity-token/', get_integrity_token),
]