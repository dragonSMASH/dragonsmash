from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from api.models import Player


class RegisterPlayerResource(serializers.Serializer):
    """ Serialize the information required to register a new Player. """
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField(required=False)
    phone = serializers.CharField()

    def create(self, validated_data):
        user = User(username=validated_data.pop('username'),
                    email=validated_data.pop('email'),
                    password=validated_data.pop('password'))
        user.full_clean()
        Token.objects.create(user=user)
        player = Player(user=user, **validated_data)
        player.full_clean()
        player.save()

        return player
