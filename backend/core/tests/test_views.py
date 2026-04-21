from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import UserProfile, ChatSession
from unittest.mock import patch

class ViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = UserProfile.objects.create(user=self.user, military_status='Мобілізований', service_type='ЗСУ')
        self.register_url = reverse('register')
        self.profile_url = reverse('user-profile')
        self.login_url = reverse('api_token_auth')
        self.chat_url = reverse('legal-chat')

    def test_register_user(self):
        data = {
            'username': 'testuser2',
            'password': 'password123',
            'email': 'test2@test.com',
            'military_status': 'Офіцер',
            'service_type': 'НГУ'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login_user(self):
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['military_status'], 'Мобілізований')

    @patch('core.views.LegalAssistantService.process_query')
    def test_legal_chat(self, mock_process_query):
        mock_process_query.return_value = {
            "answer": "You should apply for leave.",
            "sources": []
        }
        self.client.force_authenticate(user=self.user)
        data = {'question': 'How to get leave?'}
        response = self.client.post(self.chat_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['answer'], "You should apply for leave.")
        self.assertTrue(ChatSession.objects.filter(user=self.user).exists())
