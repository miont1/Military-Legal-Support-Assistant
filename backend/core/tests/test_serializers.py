from django.test import TestCase
from core.serializers import QuestionSerializer, RegistrationSerializer
from django.contrib.auth.models import User

class SerializerTests(TestCase):
    def test_registration_serializer(self):
        data = {
            'username': 'newuser',
            'password': 'password123',
            'email': 'test@test.com',
            'military_status': 'Мобілізований',
            'service_type': 'ЗСУ'
        }
        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.military_status, 'Мобілізований')

    def test_question_serializer(self):
        data = {
            'question': 'How to apply for leave?',
        }
        serializer = QuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        data_invalid = {}
        serializer_invalid = QuestionSerializer(data=data_invalid)
        self.assertFalse(serializer_invalid.is_valid())
