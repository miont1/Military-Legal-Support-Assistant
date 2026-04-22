from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from core.models import ChatSession, UserQuery
from unittest.mock import patch
from django.utils import timezone
import time

class HistoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='historyuser', password='password123')
        self.chat_url = reverse('legal-chat')
        self.sessions_url = reverse('session-list')
        self.client.force_authenticate(user=self.user)

    @patch('core.views.LegalAssistantService.process_query')
    def test_fr_3_1_1_create_session_if_not_passed(self, mock_process_query):
        """FR 3.1.1: Create new session if session_id is not passed"""
        mock_process_query.return_value = {"answer": "A", "sources": []}
        
        initial_sessions_count = ChatSession.objects.count()
        response = self.client.post(self.chat_url, {'question': 'First question without session'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ChatSession.objects.count(), initial_sessions_count + 1)
        self.assertIn('session_id', response.data)

    @patch('core.views.LegalAssistantService.process_query')
    def test_fr_3_1_2_auto_generate_title(self, mock_process_query):
        """FR 3.1.2: Title generated from first query (<50 chars)"""
        mock_process_query.return_value = {"answer": "A", "sources": []}
        
        # Query < 50 chars
        short_query = "Short query title"
        self.client.post(self.chat_url, {'question': short_query})
        session1 = ChatSession.objects.last()
        self.assertEqual(session1.title, short_query)

        # Query > 50 chars
        long_query = "This is a very long query that definitely exceeds fifty characters to test the truncation."
        self.client.post(self.chat_url, {'question': long_query})
        session2 = ChatSession.objects.last()
        self.assertTrue(len(session2.title) <= 53) # 50 chars + "..."
        self.assertEqual(session2.title, long_query[:50] + "...")

    def test_fr_3_1_3_created_at_timestamp(self):
        """FR 3.1.3: created_at timestamp in database for queries and sessions"""
        session = ChatSession.objects.create(user=self.user, title='Time Test')
        query = UserQuery.objects.create(
            user=self.user, session=session, query_text='Q', response_text='R'
        )
        self.assertIsNotNone(session.created_at)
        self.assertIsNotNone(query.created_at)
        
        # Testing API returns created_at for sessions
        response = self.client.get(self.sessions_url)
        self.assertIn('created_at', response.data[0])

    def test_fr_3_2_1_sessions_list_sorted_newest_to_oldest(self):
        """FR 3.2.1: Sessions list endpoint sorted chronologically (newest first)"""
        session1 = ChatSession.objects.create(user=self.user, title='Old Session')
        # Simulate time difference. We might need to manually update created_at or just rely on sequence
        session1.created_at = timezone.now() - timezone.timedelta(days=1)
        session1.save()
        
        session2 = ChatSession.objects.create(user=self.user, title='New Session')
        
        response = self.client.get(self.sessions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure newest is first
        sessions_data = response.data
        self.assertTrue(len(sessions_data) >= 2)
        self.assertEqual(sessions_data[0]['id'], session2.id)
        self.assertEqual(sessions_data[1]['id'], session1.id)

    def test_fr_3_2_2_full_message_history(self):
        """FR 3.2.2: Full message history for a specific session_id"""
        session = ChatSession.objects.create(user=self.user, title='History Session')
        UserQuery.objects.create(user=self.user, session=session, query_text='Q1', response_text='R1')
        UserQuery.objects.create(user=self.user, session=session, query_text='Q2', response_text='R2')
        
        session_detail_url = reverse('session-detail', kwargs={'pk': session.id})
        response = self.client.get(session_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # It should return a list of queries for the session
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['query_text'], 'Q1')
        self.assertEqual(response.data[1]['query_text'], 'Q2')

    def test_fr_3_2_3_session_deletion(self):
        """FR 3.2.3: Session deletion by ID"""
        session = ChatSession.objects.create(user=self.user, title='To Delete')
        session_detail_url = reverse('session-detail', kwargs={'pk': session.id})
        
        response = self.client.delete(session_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ChatSession.objects.filter(id=session.id).exists())

    def test_fr_3_2_4_cascade_deletion(self):
        """FR 3.2.4: Cascade deletion: delete session -> all queries deleted"""
        session = ChatSession.objects.create(user=self.user, title='Cascade Delete')
        query = UserQuery.objects.create(user=self.user, session=session, query_text='Q', response_text='R')
        
        query_id = query.id
        self.assertTrue(UserQuery.objects.filter(id=query_id).exists())
        
        # Delete session
        session.delete()
        
        # Verify query is deleted
        self.assertFalse(UserQuery.objects.filter(id=query_id).exists())
