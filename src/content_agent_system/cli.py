"""Command-line interface for content agent system."""

import asyncio
import sys
from typing import Optional

from content_agent_system.agents.base import AgentConfig
from content_agent_system.agents.writer import ContentWriterAgent
from content_agent_system.content.producer import ContentProducer
from content_agent_system.rag.knowledge_base import Document, KnowledgeBase
from content_agent_system.utils.logging import setup_logger

logger = setup_logger("content-agent-cli")


async def run_example() -> None:
    """Run an example content generation workflow."""
    logger.info("Initializing Content Agent System...")

    # Create knowledge base
    kb = KnowledgeBase(collection_name="example_kb")

    # Add some example documents
    kb.add_documents(
        [
            Document(
                id="doc1",
                content="AI and machine learning are transforming content creation.",
                metadata={"source": "tech_article"},
            ),
            Document(
                id="doc2",
                content="RAG systems combine retrieval with generation for better results.",
                metadata={"source": "research_paper"},
            ),
        ]
    )

    logger.info(f"Knowledge base initialized with {len(kb)} documents")

    # Create content writer agent
    writer_config = AgentConfig(name="content_writer", model="gpt-4", temperature=0.7)
    writer_agent = ContentWriterAgent(config=writer_config)

    # Create content producer
    producer = ContentProducer(agents=[writer_agent], knowledge_base=kb)

    logger.info(f"Content producer initialized with agents: {producer.list_agents()}")

    # Generate content with RAG
    input_data = {
        "topic": "AI in content creation",
        "style": "informative",
    }

    logger.info("Generating content...")
    result = await producer.produce(
        agent_name="content_writer", input_data=input_data, use_rag=True
    )

    logger.info("Content generated successfully!")
    print("\n" + "=" * 80)
    print("GENERATED CONTENT:")
    print("=" * 80)
    print(result["content"])
    print("=" * 80)
    print(f"\nMetadata: {result['metadata']}")


def main() -> None:
    """Main entry point for CLI."""
    try:
        asyncio.run(run_example())
        sys.exit(0)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
