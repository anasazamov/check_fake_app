from django.db import models

# Create your models here.


class Device(models.Model):
    license = models.CharField(max_length=1000, unique=True)
    status = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    limit = models.IntegerField(default=0)

    def __str__(self):
        return self.license
    
class MTT(models.Model):

    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Token(models.Model):
    mtt = models.ForeignKey(MTT, on_delete=models.CASCADE)
    token = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
    
    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        ordering = ['-created_at']
        unique_together = ('mtt', 'token')

class PhoneDevice(models.Model):

    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    model = models.CharField(max_length=250)
    manafacturer = models.CharField(max_length=250)
    device_id = models.CharField(max_length=250, unique=True)
    device_name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Phone Device'
        verbose_name_plural = 'Phone Devices'
        ordering = ['-token__created_at']
        unique_together = ('token', 'device_id')