from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length = 10)
    stdID = models.CharField(max_length = 8)
    HB = models.BooleanField(default = False)

    def __str__(self):
        return self.name
    
    objects = models.Manager()
