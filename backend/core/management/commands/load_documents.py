import json
import os
from django.core.management.base import BaseCommand
from core.models import LegalDocument
from core.patterns.singleton import VectorStoreLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Command(BaseCommand):
    help = 'Loads legal documents from a JSON file into the database and vector store'

    def handle(self, *args, **kwargs):
        file_path = 'data/documents.json'
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Initialize Vector Store
        loader = VectorStoreLoader()
        vector_store = loader.get_vector_store()
        
        if vector_store is None:
             self.stdout.write(self.style.ERROR('Failed to initialize Vector Store. Check API keys.'))
             return

        # Initialize Text Splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

        documents_to_add = []
        
        for item in data:
            # 1. Save to DB
            doc, created = LegalDocument.objects.get_or_create(
                title=item['title'],
                defaults={
                    'content': item['content'],
                    'source_url': item['source_url']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created DB record: {doc.title}'))
            else:
                self.stdout.write(f'Record already exists: {doc.title}')

            # 2. Prepare for Vector Store with Chunking
            full_text = f"{item['title']}\n{item['content']}"
            
            # Create chunks
            chunks = text_splitter.split_text(full_text)
            
            for chunk in chunks:
                metadata = {
                    "title": item['title'],
                    "source_url": item['source_url'],
                    "db_id": doc.id,
                    "category": item.get('category', ''),
                    "tags": item.get('tags', [])
                }
                documents_to_add.append(Document(page_content=chunk, metadata=metadata))

        # 3. Add to Vector Store
        if documents_to_add:
            self.stdout.write(f'Adding {len(documents_to_add)} chunks to Vector Store...')
            try:
                vector_store.add_documents(documents_to_add)
                vector_store.save_local("faiss_index")
                self.stdout.write(self.style.SUCCESS(f'Successfully added documents to Vector Store.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding to vector store: {e}'))
        else:
            self.stdout.write('No documents to add.')
