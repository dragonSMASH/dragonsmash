from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Player, PlayerData


class RegisterPlayerResource(serializers.Serializer):
    """ Serialize the information required to register a new Player. """
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField(required=False)
    phone = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def create(self, validated_data):
        player = Player.objects.create_player(validated_data.pop('username'),
                                              validated_data.pop('password'),
                                              validated_data.pop('phone'),
                                              validated_data.pop('email', None))
        PlayerData.objects.create(player=player,
                                  location=Point(validated_data.pop('longitude'),
                                                 validated_data.pop('latitude'),
                                                 srid=4326),
                                  money=0)
        Token.objects.create(user=player.user)
        return player


class PlayerLocationUpdateResource(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def update(self, instance, validated_data):
        instance.location.x = validated_data.pop('longitude')
        instance.location.y = validated_data.pop('latitude')
        instance.save()
        return instance
