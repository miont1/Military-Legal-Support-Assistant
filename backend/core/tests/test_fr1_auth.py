from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from core.models import UserProfile
from unittest.mock import patch
from django.db import InternalError, IntegrityError, transaction

class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('api_token_auth')

    def test_fr_1_1_1_registration_endpoint(self):
        """FR 1.1.1: Registration endpoint availability"""
        response = self.client.options(self.register_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_fr_1_1_2_validation_username_password_email(self):
        """FR 1.1.2: Username and password required, email optional"""
        # Missing password
        response = self.client.post(self.register_url, {'username': 'test1', 'military_status': 'Офіцер', 'service_type': 'ЗСУ'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        
        # Missing username
        response = self.client.post(self.register_url, {'password': 'pwd', 'military_status': 'Офіцер', 'service_type': 'ЗСУ'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

        # Successful registration without email
        response = self.client.post(self.register_url, {
            'username': 'testuser_no_email',
            'password': 'password123',
            'military_status': 'Офіцер',
            'service_type': 'ЗСУ'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser_no_email').exists())

    def test_fr_1_1_3_military_status_required(self):
        """FR 1.1.3: military_status is required and accepts specific values"""
        # Missing military_status
        response = self.client.post(self.register_url, {
            'username': 'test1', 'password': '123', 'service_type': 'ЗСУ'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('military_status', response.data)

        # Valid values
        statuses = ['Мобілізований', 'Контрактник', 'Строковик', 'Офіцер']
        for i, s in enumerate(statuses):
            response = self.client.post(self.register_url, {
                'username': f'user_m_{i}', 'password': '123', 'military_status': s, 'service_type': 'ЗСУ'
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(UserProfile.objects.get(user__username=f'user_m_{i}').military_status, s)

    def test_fr_1_1_4_service_type_required(self):
        """FR 1.1.4: service_type is required and accepts specific values"""
        # Missing service_type
        response = self.client.post(self.register_url, {
            'username': 'test1', 'password': '123', 'military_status': 'Офіцер'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('service_type', response.data)

        # Valid values
        services = ['ЗСУ', 'НГУ', 'ТрО', 'ДПСУ']
        for i, s in enumerate(services):
            response = self.client.post(self.register_url, {
                'username': f'user_s_{i}', 'password': '123', 'military_status': 'Офіцер', 'service_type': s
            })
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(UserProfile.objects.get(user__username=f'user_s_{i}').service_type, s)

    @patch('core.serializers.UserProfile.objects.create')
    def test_fr_1_1_5_atomicity(self, mock_create):
        """FR 1.1.5: Atomicity of User and UserProfile creation"""
        mock_create.side_effect = IntegrityError("DB Error")
        initial_user_count = User.objects.count()
        
        try:
            response = self.client.post(self.register_url, {
                'username': 'atomic_user',
                'password': 'password123',
                'military_status': 'Офіцер',
                'service_type': 'ЗСУ'
            })
        except Exception:
            pass
            
        self.assertEqual(User.objects.count(), initial_user_count)

    def test_fr_1_2_1_and_1_2_2_and_1_2_3_login(self):
        """FR 1.2.1, 1.2.2, 1.2.3: Login with username/password, token auth, returns access token"""
        User.objects.create_user(username='loginuser', password='password123')
        response = self.client.post(self.login_url, {
            'username': 'loginuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 1.2.3
        self.assertIn('token', response.data)

    def test_fr_1_2_4_login_security(self):
        """FR 1.2.4: General error message on invalid credentials"""
        User.objects.create_user(username='loginuser2', password='password123')
        response = self.client.post(self.login_url, {
            'username': 'loginuser2',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        error_msg = str(response.data['non_field_errors'][0]).lower()
        self.assertNotIn('password', error_msg)
        self.assertNotIn('not found', error_msg)
