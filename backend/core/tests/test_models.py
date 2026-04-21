from django.test import TestCase
from django.contrib.auth.models import User
from core.models import UserProfile, LegalDocument, ChatSession, UserQuery

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = UserProfile.objects.create(user=self.user, military_status='Мобілізований', service_type='ЗСУ')
        self.document = LegalDocument.objects.create(title='Test Law', content='Test Content', source_url='http://test.com')
        self.session = ChatSession.objects.create(user=self.user, title='Test Session')
        self.query = UserQuery.objects.create(
            user=self.user,
            session=self.session,
            query_text='What is the law?',
            response_text='The law is test.',
            issue_category='General',
            document_status='Є всі документи',
            situation_stage='Ситуація тільки виникла'
        )

    def test_user_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser - Мобілізований')

    def test_legal_document_str(self):
        self.assertEqual(str(self.document), 'Test Law')

    def test_chat_session_str(self):
        self.assertEqual(str(self.session), 'Test Session (testuser)')

    def test_user_query_str(self):
        self.assertTrue(str(self.query).startswith('Query at '))
