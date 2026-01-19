"""RAG knowledge base implementation with ChromaDB and HuggingFace embeddings."""

import os
from typing import List, Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

from core.config import KNOWLEDGE_BASE_DIR, VECTOR_STORE_DIR


class KnowledgeBase:
    """RAG knowledge base for content generation."""
    
    def __init__(self, collection_name: str = "content_knowledge"):
        """Initialize knowledge base with HuggingFace embeddings and ChromaDB.
        
        Args:
            collection_name: Name for the vector store collection
        """
        self.collection_name = collection_name
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store_path = os.path.join(VECTOR_STORE_DIR, collection_name)
        self.vector_store = None
        
    def load_documents(self, directory: Optional[str] = None) -> List:
        """Load documents from knowledge base directory.
        
        Args:
            directory: Specific subdirectory to load from, or None for all
            
        Returns:
            List of loaded documents
        """
        if directory:
            load_path = os.path.join(KNOWLEDGE_BASE_DIR, directory)
        else:
            load_path = KNOWLEDGE_BASE_DIR
            
        if not os.path.exists(load_path):
            print(f"Warning: Knowledge base directory not found: {load_path}")
            return []
            
        documents = []
        
        # Load .md files
        try:
            md_loader = DirectoryLoader(
                load_path,
                glob="**/*.md",
                loader_cls=TextLoader,
                show_progress=True
            )
            documents.extend(md_loader.load())
        except Exception as e:
            print(f"Warning: Could not load markdown files: {e}")
            
        # Load .txt files
        try:
            txt_loader = DirectoryLoader(
                load_path,
                glob="**/*.txt",
                loader_cls=TextLoader,
                show_progress=True
            )
            documents.extend(txt_loader.load())
        except Exception as e:
            print(f"Warning: Could not load text files: {e}")
            
        return documents
        
    def build_vector_store(self, documents: Optional[List] = None):
        """Build or update vector store from documents.
        
        Args:
            documents: List of documents to index, or None to load all
        """
        if documents is None:
            documents = self.load_documents()
            
        if not documents:
            print("Warning: No documents found to index")
            return
            
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300,
            length_function=len
        )
        splits = text_splitter.split_documents(documents)
        
        # Create vector store
        os.makedirs(self.vector_store_path, exist_ok=True)
        self.vector_store = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            persist_directory=self.vector_store_path,
            collection_name=self.collection_name
        )
        
        print(f"Indexed {len(splits)} chunks from {len(documents)} documents")
        
    def load_vector_store(self):
        """Load existing vector store from disk."""
        if os.path.exists(self.vector_store_path):
            self.vector_store = Chroma(
                persist_directory=self.vector_store_path,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
            print(f"Loaded vector store from {self.vector_store_path}")
        else:
            print(f"No existing vector store found at {self.vector_store_path}")
            print("Building new vector store...")
            self.build_vector_store()
            
    def search(self, query: str, k: int = 5) -> List[str]:
        """Search knowledge base for relevant context.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant text chunks
        """
        if self.vector_store is None:
            self.load_vector_store()
            
        if self.vector_store is None:
            print("Warning: Vector store not available")
            return []
            
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error searching vector store: {e}")
            return []
            
    def get_context(self, topic: str, lens: str, objective: str, k: int = 5) -> str:
        """Get relevant context for content generation.
        
        Args:
            topic: Content topic
            lens: Primary lens (incentives, processes, etc.)
            objective: Content objective
            k: Number of chunks to retrieve
            
        Returns:
            Combined context string
        """
        # Construct comprehensive query
        query = f"{topic} {lens} {objective}"
        
        # Search for relevant chunks
        chunks = self.search(query, k=k)
        
        if not chunks:
            return "No relevant context found in knowledge base."
            
        # Combine chunks
        context = "\n\n".join(chunks)
        return context
