from django.db import models

# Create your models here.


class Device(models.Model):
    license = models.CharField(max_length=1000, unique=True)
    status = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.license