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