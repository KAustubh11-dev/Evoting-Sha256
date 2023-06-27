from django.db import models

# Create your models here.


class Candidate(models.Model):
    adhar = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=50, unique=True)
    phone = models.BigIntegerField(unique=True)
    email = models.CharField(max_length=254, unique=True)
    profile_photo = models.ImageField(
        upload_to='media/images/profile', height_field=None, width_field=None)
    birth_date = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    adhar_photo = models.ImageField(
        upload_to='media/images/adhar', height_field=None, width_field=None, max_length=None)
    symbol_photo = models.ImageField(
        upload_to='media/images/symbol', height_field=None, width_field=None, max_length=None)

    def __int__(self):
        return self.adhar
