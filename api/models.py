from django.contrib.gis.db import models # inherits from django.db.models
from django.core.validators import RegexValidator

PhoneRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. \
                Up to 15 digits allowed.")


class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, validators=[PhoneRegex])
    created_at = models.DateTimeField(auto_now_add=True)


class UserData(models.Model):
    user = models.OneToOneField(User)
    location = models.PointField(geography=True)
    time = models.DateTimeField()
    money = models.IntegerField()
    objects = models.GeoManager()


class Dragon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # various base stats


class UserDragon(models.Model):
    user = models.ForeignKey(User)
    dragon = models.ForeignKey(Dragon)
    experience = models.IntegerField()
    # various stats
    last_laid = models.DateTimeField()


class Effect(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()


class DragonEffect(models.Model):
    user = models.ForeignKey(User)
    dragon = models.ForeignKey(UserDragon)
    effect = models.ForeignKey(Effect)


class Egg(models.Model):
    user = models.ForeignKey(User)
    dragon = models.ForeignKey(UserDragon)
    location = models.PointField(geography=True)
    # various stats
    lays_dragon_type = models.ForeignKey(Dragon)
