from django.contrib import admin
from check_app.models import Device

# Register your models here.

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('license', 'status', 'is_delete', 'created_at', 'updated_at')
    search_fields = ('license',)
    list_filter = ('status', 'is_delete')
    ordering = ('-created_at',)
    list_per_page = 20