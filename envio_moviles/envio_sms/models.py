from django.db import models

class SMSMessage(models.Model):
    number = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
