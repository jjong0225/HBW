from django.db import models

# Create your models here.


class Logging(models.Model):
    user = models.CharField(max_length=10)
    manager = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    item = models.CharField(max_length=10)
    message = models.CharField(max_length=50)
