from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.authtoken.models import Token
from .models import Player


class PlayerModelTests(TestCase):

    def test_simple_player_creation(self):
        Player.objects.create_player("shreyas", "password", "5105555555")

    def test_get_player_username(self):
        player = Player.objects.create_player("shreyas", "password", "5105555555")
        self.assertEqual(player.username, "shreyas")

    def test_get_player_email(self):
        player = Player.objects.create_player("shreyas", "password", "5105555555", "shreyas@test.com")
        self.assertEqual(player.email, "shreyas@test.com")

    def test_get_player_email_with_no_set_email(self):
        player = Player.objects.create_player("shreyas", "password", "5105555555")
        self.assertEqual(player.email, '')

    def test_get_player_auth_token(self):
        player = Player.objects.create_player("shreyas", "password", "5105555555")
        Token.objects.create(user=player.user)
        self.assertEqual(player.auth_token.key, player.user.auth_token.key)

    def test_player_duplicate_username_not_allowed(self):
        Player.objects.create_player("shreyas", "passwprd", "5105555555")
        with self.assertRaises(ValidationError):
            Player.objects.create_player("shreyas", "passwprd", "5105555554")

    def test_player_duplicate_phone_not_allowed(self):
        Player.objects.create_player("shreyas", "passwprd", "5105555555")
        with self.assertRaises(ValidationError):
            Player.objects.create_player("marvin", "passwprd", "5105555555")
