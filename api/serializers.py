from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Player


class RegisterPlayerResource(serializers.Serializer):
    """ Serialize the information required to register a new Player. """
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField(required=False)
    phone = serializers.CharField()

    def create(self, validated_data):
        player = Player.objects.create_player(validated_data.pop('username'),
                                              validated_data.pop('password'),
                                              validated_data.pop('phone'),
                                              validated_data.pop('email', None))
        Token.objects.create(user=player.user)

        return player
