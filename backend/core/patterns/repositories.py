from .singleton import VectorStoreLoader
from ..models import LegalDocument

class DocumentRepository:
    """
    Repository to abstract interactions with the FAISS vector store and database.
    """
    def __init__(self):
        self.vector_loader = VectorStoreLoader()
        self.vector_store = self.vector_loader.get_vector_store()

    def search_relevant_documents(self, query: str, k: int = 3):
        """
        Searches for relevant documents in the vector store.
        """
        if not self.vector_store:
            return []

        try:
            # docs = self.vector_store.similarity_search(query, k=k)
            # For now, let's assume the vector store works as expected from LangChain
            docs = self.vector_store.similarity_search(query, k=k)
            
            # Map LangChain Documents to our LegalDocument model (or just return objects with compatible attributes)
            results = []
            for doc in docs:
                # Assuming metadata contains title and source_url
                title = doc.metadata.get('title', 'Unknown Title')
                source_url = doc.metadata.get('source_url', '#')
                results.append(LegalDocument(title=title, content=doc.page_content, source_url=source_url))
            
            return results
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []

    def save_document(self, title, content, source_url):
        """
        Saves a document to the database (and ideally updates the vector store).
        """
        doc = LegalDocument.objects.create(title=title, content=content, source_url=source_url)
        return doc
