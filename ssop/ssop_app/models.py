from django.db import models


class User(models.Model):
    dni = models.CharField(max_length=9, null=True)
    name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name + " " + self.surname


class Company(models.Model):
    cif = models.CharField(max_length=9)
    comercial_name = models.CharField(max_length=50)
    official_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=50)
    contact_surname = models.CharField(max_length=50)


class SMSMessage(models.Model):
    number = models.CharField(max_length=20)
