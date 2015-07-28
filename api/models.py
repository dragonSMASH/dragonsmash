from django.contrib.gis.db import models  # inherits from django.db.models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

PhoneRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                            message="Phone number must be entered in the format: '+999999999'. \
                                     Up to 15 digits allowed.")


class Player(models.Model):
    user = models.OneToOneField(User, related_name="player")
    phone = models.CharField(max_length=15, validators=[PhoneRegex], unique=True)


class PlayerData(models.Model):
    player = models.OneToOneField(Player)
    location = models.PointField(geography=True)
    time = models.DateTimeField()
    money = models.IntegerField()

    objects = models.GeoManager()


class Dragon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # TODO: implement various base stats


class Effect(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()


class UserDragon(models.Model):
    player = models.ForeignKey(Player)
    dragon = models.ForeignKey(Dragon)
    experience = models.IntegerField()
    last_laid = models.DateTimeField()
    effect = models.ManyToManyField(Effect)
    # TODO: implement various stats


class Egg(models.Model):
    player = models.ForeignKey(Player)
    dragon = models.ForeignKey(UserDragon)
    location = models.PointField(geography=True)
    lays_dragon_type = models.ForeignKey(Dragon)
    # TODO: implement various stats

    objects = models.GeoManager()
