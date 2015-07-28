from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.authtoken.models import Token
from api.models import Player


class RegisterPlayerResource(serializers.Serializer):
    """ Serialize the information required to register a new Player. """
    username = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()
    # TODO: Add back optional email

    @transaction.atomic()
    def create(self, validated_data):
        user = User(username=validated_data.pop('username'),
                    password=validated_data.pop('password'))
        user.full_clean()
        user.save()
        Token.objects.create(user=user)
        player = Player(user=user, **validated_data)
        player.full_clean()
        player.save()

        return player
