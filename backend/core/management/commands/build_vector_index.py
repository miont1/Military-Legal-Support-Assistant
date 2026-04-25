import os
from django.core.management.base import BaseCommand
from core.models import LegalDocument
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Command(BaseCommand):
    help = 'Synchronizes or creates a FAISS base from documents in the PostgreSQL database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Collecting documents from the database...")
        documents = LegalDocument.objects.all()
        
        if not documents.exists():
            self.stdout.write(self.style.WARNING("No documents in the database for indexing."))
            return
            
        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

        texts = []
        metadatas = []
        
        for doc in documents:
            # If content is empty, FAISS might throw an error, so we check it
            content = doc.content.strip()
            if not content:
                self.stdout.write(self.style.WARNING(f"Skipped document '{doc.title}' due to missing text."))
                continue
                
            # Split the document into chunks
            chunks = text_splitter.split_text(content)
            
            for chunk in chunks:
                texts.append(chunk)
                # Add metadata which will be unpacked in RAG later
                metadatas.append({
                    'id': doc.id,
                    'title': doc.title,
                    'source_url': doc.source_url or '#'
                })
            
        if not texts:
            self.stdout.write(self.style.WARNING("No text available for indexing."))
            return
            
        self.stdout.write(f"Found {len(texts)} documents. Calling OpenAI to generate vectors...")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.stdout.write(self.style.ERROR("OPENAI_API_KEY variable not found. Cannot generate vectors."))
            return

        try:
            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            
            # FAISS.from_texts will automatically create a new index
            vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
            
            index_path = os.getenv("FAISS_INDEX_PATH", "faiss_index")
            vector_store.save_local(index_path)
            
            self.stdout.write(self.style.SUCCESS(f"✅ Successfully created FAISS vector store! Saved at: {index_path}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating index: {str(e)}"))
