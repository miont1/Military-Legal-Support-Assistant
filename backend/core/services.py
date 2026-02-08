from .patterns.repositories import DocumentRepository
from .patterns.adapters import OpenAIAdapter
from .models import UserQuery

class LegalAssistantService:
    """
    Service to orchestrate the RAG flow:
    Receive Query -> Embed -> Search (Repository) -> Generate Answer (Adapter) -> Save Log
    """
    def __init__(self):
        self.repository = DocumentRepository()
        self.llm_adapter = OpenAIAdapter()

    def process_query(self, query_text: str, metadata: dict = None, user_profile=None, user=None, session=None):
        # 1. Search for relevant documents
        relevant_docs = self.repository.search_relevant_documents(query_text, k=6)
        
        # 2. Prepare context from documents
        docs_context = "\n\n".join([doc.content for doc in relevant_docs])
        
        # Construct enhanced context with user profile and metadata
        context_parts = []
        
        if user_profile:
            context_parts.append(f"User Profile: Status-[{user_profile.military_status}], Service-[{user_profile.service_type}]")
        
        if metadata:
            if metadata.get('issue_category'):
                context_parts.append(f"Category: {metadata['issue_category']}")
            if metadata.get('document_status'):
                context_parts.append(f"Documents: {metadata['document_status']}")
            if metadata.get('situation_stage'):
                context_parts.append(f"Stage: {metadata['situation_stage']}")
                
        context_parts.append(f"Legal Context:\n{docs_context}")
        
        full_context = "\n".join(context_parts)
        
        # 3. Generate answer using LLM Adapter
        answer = self.llm_adapter.generate_answer(full_context, query_text)
        
        # Prepare sources data
        sources_data = [{"title": doc.title, "url": doc.source_url} for doc in relevant_docs]

        # 4. Save interaction log
        UserQuery.objects.create(
            user=user if user and user.is_authenticated else None,
            session=session,
            query_text=query_text, 
            response_text=answer,
            issue_category=metadata.get('issue_category') if metadata else None,
            document_status=metadata.get('document_status') if metadata else None,
            situation_stage=metadata.get('situation_stage') if metadata else None,
            sources=sources_data
        )
        
        return {
            "answer": answer,
            "sources": sources_data
        }
