"""Tests for retriever."""

import pytest

from content_agent_system.rag.knowledge_base import Document, KnowledgeBase
from content_agent_system.rag.retriever import Retriever


def test_retriever_initialization():
    """Test retriever initialization."""
    kb = KnowledgeBase()
    retriever = Retriever(knowledge_base=kb)
    assert retriever.knowledge_base == kb


def test_retrieve():
    """Test retrieving documents."""
    kb = KnowledgeBase()
    docs = [
        Document(id=f"doc{i}", content=f"Content {i}") for i in range(10)
    ]
    kb.add_documents(docs)

    retriever = Retriever(knowledge_base=kb)
    results = retriever.retrieve("test query", top_k=3)
    assert len(results) == 3


def test_retrieve_with_scores():
    """Test retrieving documents with scores."""
    kb = KnowledgeBase()
    docs = [
        Document(id=f"doc{i}", content=f"Content {i}") for i in range(5)
    ]
    kb.add_documents(docs)

    retriever = Retriever(knowledge_base=kb)
    results = retriever.retrieve_with_scores("test query", top_k=3)
    assert len(results) == 3
    assert all(isinstance(r[0], Document) for r in results)
    assert all(isinstance(r[1], float) for r in results)
