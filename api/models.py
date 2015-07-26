from django.contrib.gis.db import models # inherits from django.db.models
from django.core.validators import RegexValidator

PhoneRegex = lambda: RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, validators=[PhoneRegex()])
    created_at = models.DateTimeField(auto_now_add=True)

class UserData(models.Model):
    user = models.OneToOneField(User)
    location = models.PointField(geography=True)
    time = models.DateTimeField()
    money = models.IntegerField()

    objects = models.GeoManager()
