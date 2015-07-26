# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.gis.geos import GEOSGeometry
from datetime import datetime, timezone, timedelta

def seed_user_data(apps, schema_editor):
    User = apps.get_model("api", "User")

    user1 = User()
    user1.username = "chandsie"
    user1.email = "shreyas.chand@gmail.com"
    user1.phone = "5105555555"
    user1.save()

    user2 = User()
    user2.username = "zhangmarvin"
    user2.email = "zhangmarvin95@gmail.com"
    user2.phone = "5105555554"
    user2.save()

    user3 = User()
    user3.username = "bhou"
    user3.email = "brian.hou@berkeley.edu"
    user3.phone = "5105555553"
    user3.save()

    user4 = User()
    user4.username = "derbear"
    user4.email = "derek.leung@berkeley.edu"
    user4.phone = "5105555552"
    user4.save()

def seed_location_data(apps, schema_editor):
    User = apps.get_model("api", "User")
    UserData = apps.get_model("api", "UserData")

    farm = GEOSGeometry('POINT(-122.1712559 37.4282631)', srid=4326)
    cal  = GEOSGeometry('POINT(-122.2590136 37.8710770)', srid=4326)

    u1 = User.objects.all()[0]
    u2 = User.objects.all()[1]

    ud1 = UserData()
    ud1.user = u1
    ud1.location = cal
    ud1.time = datetime.now(tz=timezone(-timedelta(hours=8)))
    ud1.money = 90
    ud1.save()

    ud2 = UserData()
    ud2.user = u2
    ud2.location = farm
    ud2.time = datetime.now(tz=timezone(-timedelta(hours=8)))
    ud2.money = 20
    ud2.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_user_data),
        migrations.RunPython(seed_location_data)
    ]


