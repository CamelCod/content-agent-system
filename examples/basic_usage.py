"""Example usage of the content agent system."""

import asyncio

from content_agent_system.agents.base import AgentConfig
from content_agent_system.agents.writer import ContentWriterAgent
from content_agent_system.content.producer import ContentProducer
from content_agent_system.rag.knowledge_base import Document, KnowledgeBase


async def basic_example():
    """Basic example without RAG."""
    print("=" * 80)
    print("BASIC CONTENT GENERATION (WITHOUT RAG)")
    print("=" * 80)

    # Create a content writer agent
    config = AgentConfig(name="basic_writer", model="gpt-4", temperature=0.7)
    writer = ContentWriterAgent(config=config)

    # Create content producer
    producer = ContentProducer(agents=[writer])

    # Generate content
    result = await producer.produce(
        agent_name="basic_writer",
        input_data={
            "topic": "Benefits of AI in Healthcare",
            "style": "educational",
        },
    )

    print(f"\nGenerated Content:\n{result['content']}\n")
    print(f"Metadata: {result['metadata']}\n")


async def rag_example():
    """Example with RAG (Retrieval-Augmented Generation)."""
    print("=" * 80)
    print("CONTENT GENERATION WITH RAG")
    print("=" * 80)

    # Create knowledge base
    kb = KnowledgeBase(collection_name="healthcare_kb")

    # Add documents to knowledge base
    documents = [
        Document(
            id="doc1",
            content="AI in healthcare improves diagnosis accuracy by analyzing medical images.",
            metadata={"category": "diagnostics", "source": "medical_journal"},
        ),
        Document(
            id="doc2",
            content="Machine learning models can predict patient outcomes and personalize treatment plans.",
            metadata={"category": "prediction", "source": "research_paper"},
        ),
        Document(
            id="doc3",
            content="AI-powered chatbots provide 24/7 patient support and triage services.",
            metadata={"category": "patient_care", "source": "tech_review"},
        ),
    ]
    kb.add_documents(documents)
    print(f"\nKnowledge Base initialized with {len(kb)} documents\n")

    # Create content writer agent
    config = AgentConfig(name="rag_writer", model="gpt-4", temperature=0.7)
    writer = ContentWriterAgent(config=config)

    # Create content producer with knowledge base
    producer = ContentProducer(agents=[writer], knowledge_base=kb)

    # Generate content with RAG
    result = await producer.produce(
        agent_name="rag_writer",
        input_data={
            "topic": "AI Applications in Healthcare",
            "style": "informative",
        },
        use_rag=True,
    )

    print(f"\nGenerated Content (with RAG context):\n{result['content']}\n")
    print(f"Metadata: {result['metadata']}\n")


async def multi_agent_example():
    """Example with multiple agents."""
    print("=" * 80)
    print("MULTI-AGENT CONTENT PRODUCTION")
    print("=" * 80)

    # Create multiple agents with different configurations
    technical_config = AgentConfig(
        name="technical_writer", model="gpt-4", temperature=0.5
    )
    creative_config = AgentConfig(
        name="creative_writer", model="gpt-4", temperature=0.9
    )

    technical_writer = ContentWriterAgent(config=technical_config)
    creative_writer = ContentWriterAgent(config=creative_config)

    # Create content producer with multiple agents
    producer = ContentProducer(agents=[technical_writer, creative_writer])

    print(f"\nAvailable agents: {producer.list_agents()}\n")

    # Generate technical content
    technical_result = await producer.produce(
        agent_name="technical_writer",
        input_data={
            "topic": "Neural Network Architecture",
            "style": "technical",
        },
    )
    print(f"Technical Content:\n{technical_result['content']}\n")

    # Generate creative content
    creative_result = await producer.produce(
        agent_name="creative_writer",
        input_data={
            "topic": "The Future of AI",
            "style": "creative",
        },
    )
    print(f"\nCreative Content:\n{creative_result['content']}\n")


async def main():
    """Run all examples."""
    await basic_example()
    print("\n")
    await rag_example()
    print("\n")
    await multi_agent_example()


if __name__ == "__main__":
    asyncio.run(main())
