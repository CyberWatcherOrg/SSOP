from django.db import models

# Create your models here.


class SMSMessage(models.Model):
    numero = models.CharField(max_length=200)
    mensaje = models.CharField(max_length=1000)