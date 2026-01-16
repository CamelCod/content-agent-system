"""Knowledge base for RAG (Retrieval-Augmented Generation) system."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Document model for knowledge base."""

    id: str = Field(..., description="Unique document identifier")
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")


class KnowledgeBase:
    """Knowledge base for storing and retrieving documents using RAG."""

    def __init__(self, collection_name: str = "default") -> None:
        """Initialize the knowledge base.

        Args:
            collection_name: Name of the collection to use
        """
        self.collection_name = collection_name
        self.documents: List[Document] = []

    def add_document(self, document: Document) -> None:
        """Add a document to the knowledge base.

        Args:
            document: Document to add
        """
        self.documents.append(document)

    def add_documents(self, documents: List[Document]) -> None:
        """Add multiple documents to the knowledge base.

        Args:
            documents: List of documents to add
        """
        self.documents.extend(documents)

    def search(
        self, query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Search for relevant documents.

        Args:
            query: Search query
            top_k: Number of results to return
            filters: Optional filters for metadata

        Returns:
            List of relevant documents
        """
        # Placeholder for actual vector search implementation
        # In production, this would use ChromaDB or similar vector database
        results = self.documents[:top_k]
        return results

    def delete_document(self, document_id: str) -> bool:
        """Delete a document from the knowledge base.

        Args:
            document_id: ID of document to delete

        Returns:
            True if document was deleted, False otherwise
        """
        initial_length = len(self.documents)
        self.documents = [doc for doc in self.documents if doc.id != document_id]
        return len(self.documents) < initial_length

    def clear(self) -> None:
        """Clear all documents from the knowledge base."""
        self.documents.clear()

    def __len__(self) -> int:
        """Return the number of documents in the knowledge base."""
        return len(self.documents)

    def __repr__(self) -> str:
        """String representation of the knowledge base."""
        return f"KnowledgeBase(collection={self.collection_name}, documents={len(self.documents)})"
