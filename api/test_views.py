from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class StatusTests(APITestCase):

    def test_status_view(self):
        response = self.client.get(reverse("api/v1:status"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "howdy, partner!"})


class RegisterTests(APITestCase):
    register_url = reverse("api/v1:register")

    def test_user_registration_with_valid_data(self):
        user_info = {"username": "shreyas", "password": "password", "phone": "5105555555", "email": "shreyas@test.com"}
        response = self.client.post(self.register_url, user_info)
        created_user = User.objects.get(username="shreyas")
        expected_response_token = created_user.auth_token.key
        expected_response_user_id = created_user.player.id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"auth_token": expected_response_token, "player_id": expected_response_user_id})

    def test_user_registration_with_valid_data_and_no_email(self):
        user_info = {"username": "shreyas", "password": "password", "phone": "5105555555"}
        response = self.client.post(self.register_url, user_info)
        created_user = User.objects.get(username="shreyas")
        expected_response_token = created_user.auth_token.key
        expected_response_user_id = created_user.player.id
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"auth_token": expected_response_token, "player_id": expected_response_user_id})

    def test_user_registration_with_no_username(self):
        user_info = {"password": "password",  "phone": "5105555555"}
        response = self.client.post(self.register_url, user_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": {"username": ["This field is required."]}})

    def test_user_registration_with_no_password(self):
        user_info = {"username": "shreyas", "phone": "5105555555"}
        response = self.client.post(self.register_url, user_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": {"password": ["This field is required."]}})

    def test_user_registration_with_no_phone(self):
        user_info = {"username": "shreyas", "password": "password"}
        response = self.client.post(self.register_url, user_info)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": {"phone": ["This field is required."]}})
