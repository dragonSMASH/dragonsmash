from django.core.exceptions import ValidationError
from django.test import TestCase
from api.models import *


class PlayerModelTests(TestCase):

    def test_simple_player_creation(self):
        Player.objects.create_player("shreyas", "password", "5105555555")

    def test_player_duplicate_username_not_allowed(self):
        Player.objects.create_player("shreyas", "passwprd", "5105555555")
        with self.assertRaises(ValidationError):
            Player.objects.create_player("shreyas", "passwprd", "5105555554")

    def test_player_duplicate_phone_not_allowed(self):
        Player.objects.create_player("shreyas", "passwprd", "5105555555")
        with self.assertRaises(ValidationError):
            Player.objects.create_player("marvin", "passwprd", "5105555555")
