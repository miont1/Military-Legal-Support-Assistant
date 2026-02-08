import threading
# import faiss # Mocking faiss for this example as per requirements context
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings

class VectorStoreLoader:
    """
    Singleton class to ensure the FAISS index and Embedding Model 
    are loaded into memory only once at startup.
    """
    _instance = None
    _lock = threading.Lock()
    _vector_store = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(VectorStoreLoader, cls).__new__(cls)
        return cls._instance

    def get_vector_store(self):
        """
        Lazy loads and returns the vector store instance.
        """
        if self._vector_store is None:
            from langchain_community.vectorstores import FAISS
            from langchain_openai import OpenAIEmbeddings
            import os

            embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
            
            index_path = "faiss_index"
            if os.path.exists(index_path):
                self._vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
            else:
                # Create a new empty index if it doesn't exist
                # FAISS requires at least one text to initialize, so we add a dummy one or handle it
                # For simplicity, we'll initialize with a placeholder if needed, or just return None and handle in repo
                try:
                    self._vector_store = FAISS.from_texts(["Initial setup document"], embeddings)
                    self._vector_store.save_local(index_path)
                except Exception as e:
                    print(f"Error creating initial vector store: {e}")
                    self._vector_store = None
                    
        return self._vector_store
