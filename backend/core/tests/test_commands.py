from django.test import TestCase
from django.core.management import call_command
from unittest.mock import patch, mock_open
from core.models import LegalDocument
from io import StringIO
import os

class CommandTests(TestCase):
    @patch('core.management.commands.load_documents.os.path.exists')
    @patch('core.management.commands.load_documents.open', new_callable=mock_open, read_data='[{"title": "Test Title", "content": "Test Content", "source_url": "http://test.com"}]')
    def test_load_documents_success(self, mock_file, mock_exists):
        """Test if the load_documents command successfully imports a document"""
        mock_exists.return_value = True
        
        out = StringIO()
        call_command('load_documents', stdout=out)
        
        self.assertEqual(LegalDocument.objects.count(), 1)
        self.assertEqual(LegalDocument.objects.first().title, "Test Title")
        self.assertIn('Documents loaded successfully.', out.getvalue())

    @patch('core.management.commands.load_documents.os.path.exists')
    def test_load_documents_file_not_found(self, mock_exists):
        """Test behavior when documents.json is missing"""
        mock_exists.return_value = False
        
        out = StringIO()
        call_command('load_documents', stdout=out)
        
        self.assertEqual(LegalDocument.objects.count(), 0)
        self.assertIn('File not found', out.getvalue())

    @patch('core.management.commands.build_vector_index.os.getenv')
    @patch('core.management.commands.build_vector_index.FAISS')
    @patch('core.management.commands.build_vector_index.OpenAIEmbeddings')
    def test_build_vector_index_success(self, mock_embeddings, mock_faiss, mock_getenv):
        """Test successful execution of build_vector_index"""
        # Set up necessary database states
        LegalDocument.objects.create(title='T1', content='C1', source_url='http://u.c')
        
        # Mock environment return values
        mock_getenv.side_effect = lambda key, def_val=None: 'dummy-key' if key == "OPENAI_API_KEY" else 'dummy_path'

        # Set up deep mock for FAISS behavior
        mock_vector_store = mock_faiss.from_texts.return_value
        
        out = StringIO()
        call_command('build_vector_index', stdout=out)
        
        mock_faiss.from_texts.assert_called_once()
        mock_vector_store.save_local.assert_called_once_with('dummy_path')
        self.assertIn('Successfully created FAISS vector store!', out.getvalue())

    @patch('core.management.commands.build_vector_index.os.getenv')
    def test_build_vector_index_no_api_key(self, mock_getenv):
        """Test build_vector_index when OPENAI_API_KEY is missing"""
        LegalDocument.objects.create(title='T1', content='C1', source_url='http://u.c')
        
        # Ensure env returns None for API key
        mock_getenv.return_value = None
        
        out = StringIO()
        call_command('build_vector_index', stdout=out)
        
        self.assertIn('OPENAI_API_KEY variable not found.', out.getvalue())

    def test_build_vector_index_no_documents(self):
        """Test build_vector_index when the database is empty"""
        # Note: LegalDocument table is naturally empty at the start of this test
        out = StringIO()
        call_command('build_vector_index', stdout=out)
        
        self.assertIn('No documents in the database for indexing.', out.getvalue())
