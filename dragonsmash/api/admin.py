from django.contrib import admin
from django.conf import settings
from .models import *

if settings.DEBUG:
    admin.site.register(Player)
    admin.site.register(PlayerData)
    admin.site.register(Dragon)
    admin.site.register(PlayerDragon)
    admin.site.register(Effect)
    admin.site.register(Egg)
