"""Tests for knowledge base."""

import pytest

from content_agent_system.rag.knowledge_base import Document, KnowledgeBase


def test_knowledge_base_initialization():
    """Test knowledge base initialization."""
    kb = KnowledgeBase(collection_name="test_collection")
    assert kb.collection_name == "test_collection"
    assert len(kb) == 0


def test_add_document():
    """Test adding a document."""
    kb = KnowledgeBase()
    doc = Document(id="doc1", content="Test content")
    kb.add_document(doc)
    assert len(kb) == 1


def test_add_documents():
    """Test adding multiple documents."""
    kb = KnowledgeBase()
    docs = [
        Document(id="doc1", content="Content 1"),
        Document(id="doc2", content="Content 2"),
    ]
    kb.add_documents(docs)
    assert len(kb) == 2


def test_search():
    """Test searching documents."""
    kb = KnowledgeBase()
    docs = [
        Document(id=f"doc{i}", content=f"Content {i}") for i in range(10)
    ]
    kb.add_documents(docs)

    results = kb.search("test query", top_k=5)
    assert len(results) == 5


def test_delete_document():
    """Test deleting a document."""
    kb = KnowledgeBase()
    doc = Document(id="doc1", content="Test content")
    kb.add_document(doc)
    assert len(kb) == 1

    deleted = kb.delete_document("doc1")
    assert deleted is True
    assert len(kb) == 0


def test_delete_nonexistent_document():
    """Test deleting a nonexistent document."""
    kb = KnowledgeBase()
    deleted = kb.delete_document("nonexistent")
    assert deleted is False


def test_clear():
    """Test clearing all documents."""
    kb = KnowledgeBase()
    docs = [Document(id=f"doc{i}", content=f"Content {i}") for i in range(5)]
    kb.add_documents(docs)
    assert len(kb) == 5

    kb.clear()
    assert len(kb) == 0


def test_knowledge_base_repr():
    """Test knowledge base string representation."""
    kb = KnowledgeBase(collection_name="test")
    assert "KnowledgeBase" in repr(kb)
    assert "test" in repr(kb)
