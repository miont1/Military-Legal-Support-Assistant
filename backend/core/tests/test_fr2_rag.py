from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from core.models import ChatSession
from core.services import LegalAssistantService
from unittest.mock import patch, MagicMock

class RAGTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='raguser', password='password123')
        self.chat_url = reverse('legal-chat')
        self.client.force_authenticate(user=self.user)

    def test_fr_2_1_1_text_query_and_length_limit(self):
        """FR 2.1.1: Submit text query, negative test >1000 chars"""
        # Negative test: > 1000 chars
        long_query = "a" * 1001
        response = self.client.post(self.chat_url, {'question': long_query})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('question', response.data)

        # Positive test: Valid text query
        with patch('core.views.LegalAssistantService.process_query') as mock_process:
            mock_process.return_value = {"answer": "Short answer", "sources": []}
            response = self.client.post(self.chat_url, {'question': 'Valid short query'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('core.views.LegalAssistantService.process_query')
    def test_fr_2_1_2_pass_session_id_and_issue_category(self, mock_process_query):
        """FR 2.1.2: Pass session_id and issue_category in API"""
        mock_process_query.return_value = {"answer": "Test", "sources": []}
        session = ChatSession.objects.create(user=self.user, title='Test Session')
        
        response = self.client.post(self.chat_url, {
            'question': 'How to get leave?',
            'session_id': session.id,
            'issue_category': 'Відпустка'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        mock_process_query.assert_called_once()
        args, kwargs = mock_process_query.call_args
        self.assertEqual(args[0], 'How to get leave?')
        self.assertEqual(args[1]['issue_category'], 'Відпустка')
        self.assertEqual(kwargs['session'].id, session.id)

    @patch('core.services.DocumentRepository.search_relevant_documents')
    @patch('core.services.OpenAIAdapter.generate_answer')
    def test_fr_2_1_3_and_2_1_4_semantic_search_and_llm(self, mock_generate_answer, mock_search):
        """FR 2.1.3: Semantic search initiated. FR 2.1.4: LLM receives context"""
        # Mock search results
        mock_doc1 = MagicMock(content="Doc 1 Content", title="Law 1", source_url="http://law1.com")
        mock_search.return_value = [mock_doc1]
        
        # Mock LLM generation
        mock_generate_answer.return_value = "Generated answer from LLM"
        
        service = LegalAssistantService()
        result = service.process_query("What is the law?")
        
        # FR 2.1.3: Semantic search initiated
        mock_search.assert_called_once_with("What is the law?", k=6)
        
        # FR 2.1.4: LLM receives found context
        mock_generate_answer.assert_called_once()
        context_arg, query_arg = mock_generate_answer.call_args[0]
        self.assertIn("Doc 1 Content", context_arg)
        self.assertEqual(query_arg, "What is the law?")

    @patch('core.services.DocumentRepository.search_relevant_documents')
    @patch('core.services.OpenAIAdapter.generate_answer')
    def test_fr_2_1_5_answer_structure(self, mock_generate_answer, mock_search):
        """FR 2.1.5: Answer contains answer and sources list with name and URL"""
        mock_doc1 = MagicMock(content="Content 1", title="Law Title 1", source_url="http://url1.com")
        mock_doc2 = MagicMock(content="Content 2", title="Law Title 2", source_url="http://url2.com")
        mock_search.return_value = [mock_doc1, mock_doc2]
        mock_generate_answer.return_value = "This is the generated answer."
        
        service = LegalAssistantService()
        result = service.process_query("Query")
        
        self.assertIn("answer", result)
        self.assertIn("sources", result)
        self.assertEqual(result["answer"], "This is the generated answer.")
        self.assertEqual(len(result["sources"]), 2)
        
        source1 = result["sources"][0]
        self.assertEqual(source1["title"], "Law Title 1")
        self.assertEqual(source1["url"], "http://url1.com")
