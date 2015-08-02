from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Player


class StatusTests(APITestCase):

    def test_status_view(self):
        response = self.client.get(reverse("api/v1:status"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "howdy, partner!"})


class RegisterTests(APITestCase):
    register_url = reverse("api/v1:register")

    def test_player_registration_with_valid_data(self):
        player_info = {"username": "shreyas", "password": "password", "phone": "5105555555", "email": "shreyas@test.com"}
        response = self.client.post(self.register_url, player_info)
        created_user = User.objects.get(username="shreyas")
        expected_response_token = created_user.auth_token.key
        expected_response_player_id = created_user.player.id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"token": expected_response_token, "player_id": expected_response_player_id})

    def test_player_registration_with_valid_data_and_no_email(self):
        player_info = {"username": "shreyas", "password": "password", "phone": "5105555555"}
        response = self.client.post(self.register_url, player_info)
        created_user = User.objects.get(username="shreyas")
        expected_response_token = created_user.auth_token.key
        expected_response_player_id = created_user.player.id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"token": expected_response_token, "player_id": expected_response_player_id})

    def test_player_registration_with_no_username(self):
        player_info = {"password": "password",  "phone": "5105555555"}
        response = self.client.post(self.register_url, player_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": {"username": ["This field is required."]}})

    def test_player_registration_with_no_password(self):
        player_info = {"username": "shreyas", "phone": "5105555555"}
        response = self.client.post(self.register_url, player_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": {"password": ["This field is required."]}})

    def test_player_registration_with_no_phone(self):
        player_info = {"username": "shreyas", "password": "password"}
        response = self.client.post(self.register_url, player_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": {"phone": ["This field is required."]}})


class LoginTests(APITestCase):
    login_url = reverse("api/v1:login")

    def test_player_login_with_valid_password(self):
        player = Player.objects.create_player("shreyas", "password", "5105555555")
        player_creds = {"username": "shreyas", "password": "password"}
        response = self.client.post(self.login_url, player_creds)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"token": player.user.auth_token.key})


class LogoutTests(APITestCase):
    logout_url = reverse("api/v1:logout")

    @classmethod
    def setUpClass(cls):
        cls.player = Player.objects.create_player("shreyas", "password", "5105555555")
        cls.token = Token.objects.create(user=cls.player.user)

    @classmethod
    def tearDownClass(cls):
        cls.player.delete()

    def test_player_logout_with_no_credentials(self):
        self.client.credentials()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'message': 'Authentication credentials were not provided.'})

    def test_player_logout_with_valid_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'logout successful'})

    def test_player_logout_request_with_old_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'logout successful'})
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'message': 'Invalid token.'})
