from django.db import models

# Create your models here.


class Voter(models.Model):
    adhar = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=50, unique=True)
    phone = models.BigIntegerField(unique=True)
    email = models.CharField(max_length=254, unique=True)
    profile_photo = models.ImageField(
        upload_to='images/profile')
    birth_date = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    adhar_photo = models.ImageField(
        upload_to='images/adhar')

    def __int__(self):
        return self.adhar
