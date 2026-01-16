"""Streamlit web UI for content agent system."""

import streamlit as st
from datetime import datetime
from typing import Dict

from agents.linkedin_agent import LinkedInAgent
from agents.blog_agent import BlogAgent
from agents.article_agent import ArticleAgent
from agents.validator_agent import ValidatorAgent
from core.knowledge_base import KnowledgeBase
from core.config import LENSES, OBJECTIVES, MODELS, MIN_SCORE
from batch_processor import BatchProcessor, CONTENT_CALENDAR


# Page configuration
st.set_page_config(
    page_title="Content Agent System",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables."""
    if "content_history" not in st.session_state:
        st.session_state.content_history = []
    if "knowledge_base" not in st.session_state:
        st.session_state.knowledge_base = None


def get_knowledge_base() -> KnowledgeBase:
    """Get or create knowledge base."""
    if st.session_state.knowledge_base is None:
        with st.spinner("Initializing knowledge base..."):
            kb = KnowledgeBase()
            try:
                kb.load_vector_store()
            except Exception as e:
                st.warning(f"Knowledge base not available: {e}")
            st.session_state.knowledge_base = kb
    return st.session_state.knowledge_base


def add_to_history(content: str, metadata: Dict):
    """Add content to history."""
    entry = {
        "content": content,
        "metadata": metadata,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.content_history.insert(0, entry)
    
    # Keep only last 50 entries
    if len(st.session_state.content_history) > 50:
        st.session_state.content_history = st.session_state.content_history[:50]


def display_validation(score: float, feedback: str, word_count: int):
    """Display validation results."""
    passed = score >= MIN_SCORE
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if passed:
            st.success(f"✓ Score: {score:.1f}/10")
        else:
            st.error(f"✗ Score: {score:.1f}/10")
            
    with col2:
        st.info(f"Words: {word_count}")
        
    with col3:
        status = "PASSED" if passed else "NEEDS IMPROVEMENT"
        st.metric("Status", status)
        
    with st.expander("Validation Feedback"):
        st.text(feedback)


def linkedin_post_generator():
    """LinkedIn post generator interface."""
    st.header("📱 LinkedIn Post Generator")
    
    # Mode selection
    mode = st.radio(
        "Generation Mode",
        ["Custom Topic", "Calendar Mode"],
        horizontal=True
    )
    
    if mode == "Custom Topic":
        # Custom inputs
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_area(
                "Topic",
                placeholder="Enter your post topic...",
                height=100
            )
            lens = st.selectbox("Primary Lens", LENSES)
            
        with col2:
            objective = st.selectbox("Objective", OBJECTIVES)
            model = st.selectbox("Model", list(MODELS.keys()), index=0)
            use_rag = st.checkbox("Use RAG", value=True)
            
        if st.button("Generate Post", type="primary"):
            if not topic:
                st.error("Please enter a topic")
                return
                
            with st.spinner("Generating LinkedIn post..."):
                try:
                    # Initialize agents
                    kb = get_knowledge_base() if use_rag else None
                    agent = LinkedInAgent(model=MODELS[model], knowledge_base=kb)
                    validator = ValidatorAgent(model=MODELS[model])
                    
                    # Generate
                    content = agent.generate(topic, lens, objective, use_rag=use_rag)
                    
                    # Validate
                    score, feedback, word_count = validator.validate(
                        content, "LinkedIn", "150-250"
                    )
                    
                    # Display
                    st.subheader("Generated Post")
                    st.text_area("Content", content, height=300)
                    
                    display_validation(score, feedback, word_count)
                    
                    # Save to history
                    metadata = {
                        "type": "LinkedIn",
                        "topic": topic,
                        "lens": lens,
                        "objective": objective,
                        "score": score,
                        "word_count": word_count
                    }
                    add_to_history(content, metadata)
                    
                    # Copy button
                    st.button("📋 Copy to Clipboard")
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    
    else:  # Calendar Mode
        st.info("Generate posts from pre-defined content calendar (Week 2-4)")
        
        # Calendar selection
        calendar_options = [
            f"Post {entry['post_number']} - {entry['topic']}"
            for entry in CONTENT_CALENDAR
        ]
        
        selected = st.selectbox("Select Calendar Entry", calendar_options)
        selected_post_number = int(selected.split()[1])
        entry = next(
            (e for e in CONTENT_CALENDAR if e.get("post_number") == selected_post_number),
            None,
        )
        if entry is None:
            st.error("Selected calendar entry could not be found. Please check the content calendar configuration.")
            return
        
        # Show details
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Week:** {entry['week']}")
            st.write(f"**Lens:** {entry['lens']}")
        with col2:
            st.write(f"**Objective:** {entry['objective']}")
            st.write(f"**Description:** {entry['description']}")
            
        model = st.selectbox("Model", list(MODELS.keys()), index=0, key="cal_model")
        
        if st.button("Generate from Calendar", type="primary"):
            with st.spinner("Generating LinkedIn post..."):
                try:
                    kb = get_knowledge_base()
                    agent = LinkedInAgent(model=MODELS[model], knowledge_base=kb)
                    validator = ValidatorAgent(model=MODELS[model])
                    
                    content = agent.generate_from_calendar(entry)
                    score, feedback, word_count = validator.validate(
                        content, "LinkedIn", "150-250"
                    )
                    
                    st.subheader("Generated Post")
                    st.text_area("Content", content, height=300, key="cal_content")
                    
                    display_validation(score, feedback, word_count)
                    
                    metadata = {
                        "type": "LinkedIn",
                        "post_number": entry["post_number"],
                        "topic": entry["topic"],
                        "lens": entry["lens"],
                        "objective": entry["objective"],
                        "score": score,
                        "word_count": word_count
                    }
                    add_to_history(content, metadata)
                    
                except Exception as e:
                    st.error(f"Error: {e}")


def blog_post_generator():
    """Blog post generator interface."""
    st.header("📝 Blog Post Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_area(
            "Topic",
            placeholder="Enter your blog post topic...",
            height=100
        )
        lens = st.selectbox("Primary Lens", LENSES, key="blog_lens")
        
    with col2:
        objective = st.selectbox("Objective", OBJECTIVES, key="blog_obj")
        model = st.selectbox("Model", list(MODELS.keys()), index=0, key="blog_model")
        use_rag = st.checkbox("Use RAG", value=True, key="blog_rag")
        
    if st.button("Generate Blog Post", type="primary"):
        if not topic:
            st.error("Please enter a topic")
            return
            
        with st.spinner("Generating blog post (this may take a minute)..."):
            try:
                kb = get_knowledge_base() if use_rag else None
                agent = BlogAgent(model=MODELS[model], knowledge_base=kb)
                validator = ValidatorAgent(model=MODELS[model])
                
                content = agent.generate(topic, lens, objective, use_rag=use_rag)
                score, feedback, word_count = validator.validate(
                    content, "Blog", "800-1500"
                )
                
                st.subheader("Generated Blog Post")
                st.text_area("Content", content, height=400)
                
                display_validation(score, feedback, word_count)
                
                metadata = {
                    "type": "Blog",
                    "topic": topic,
                    "lens": lens,
                    "objective": objective,
                    "score": score,
                    "word_count": word_count
                }
                add_to_history(content, metadata)
                
            except Exception as e:
                st.error(f"Error: {e}")


def article_generator():
    """Article generator interface."""
    st.header("📄 Article Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_area(
            "Topic",
            placeholder="Enter your article topic...",
            height=100
        )
        lens = st.selectbox("Primary Lens", LENSES, key="article_lens")
        
    with col2:
        objective = st.selectbox("Objective", OBJECTIVES, key="article_obj")
        model = st.selectbox("Model", list(MODELS.keys()), index=0, key="article_model")
        use_rag = st.checkbox("Use RAG", value=True, key="article_rag")
        
    if st.button("Generate Article", type="primary"):
        if not topic:
            st.error("Please enter a topic")
            return
            
        with st.spinner("Generating article (this may take 1-2 minutes)..."):
            try:
                kb = get_knowledge_base() if use_rag else None
                agent = ArticleAgent(model=MODELS[model], knowledge_base=kb)
                validator = ValidatorAgent(model=MODELS[model])
                
                content = agent.generate(topic, lens, objective, use_rag=use_rag)
                score, feedback, word_count = validator.validate(
                    content, "Article", "1000-2000"
                )
                
                st.subheader("Generated Article")
                st.text_area("Content", content, height=500)
                
                display_validation(score, feedback, word_count)
                
                metadata = {
                    "type": "Article",
                    "topic": topic,
                    "lens": lens,
                    "objective": objective,
                    "score": score,
                    "word_count": word_count
                }
                add_to_history(content, metadata)
                
            except Exception as e:
                st.error(f"Error: {e}")


def batch_processor_ui():
    """Batch processor interface."""
    st.header("🚀 Batch Processor")
    
    st.info("""
    Generate multiple LinkedIn posts from the content calendar.
    Posts will be automatically validated and retried if needed.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_post = st.number_input("Start Post", min_value=4, max_value=12, value=4)
        model = st.selectbox("Model", list(MODELS.keys()), index=0, key="batch_model")
        
    with col2:
        end_post = st.number_input("End Post", min_value=4, max_value=12, value=12)
        max_retries = st.number_input("Max Retries", min_value=1, max_value=5, value=3)
        
    if st.button("Start Batch Processing", type="primary"):
        if start_post > end_post:
            st.error("Start post must be <= end post")
            return
            
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            kb = get_knowledge_base()
            processor = BatchProcessor(
                model=MODELS[model],
                knowledge_base=kb,
                max_retries=max_retries
            )
            
            # Filter calendar
            entries = [
                e for e in CONTENT_CALENDAR
                if start_post <= e["post_number"] <= end_post
            ]
            
            results = []
            total = len(entries)
            
            for i, entry in enumerate(entries):
                status_text.text(f"Processing Post {entry['post_number']}/{end_post}...")
                
                result = processor.process_single(entry)
                results.append(result)
                
                progress_bar.progress((i + 1) / total)
                
            # Display results
            st.success(f"Batch processing complete! Generated {len(results)} posts.")
            
            # Summary table
            st.subheader("Results Summary")
            
            summary_data = []
            for r in results:
                summary_data.append({
                    "Post": r["post_number"],
                    "Topic": r["topic"][:50] + "...",
                    "Score": f"{r['score']:.1f}",
                    "Status": "✓" if r["passed"] else "✗",
                    "Attempts": r["attempts"]
                })
            
            st.table(summary_data)
            
            # Export
            output_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            processor.export_results(results, output_file)
            
            st.success(f"Results exported to {output_file}")
            
            # Show individual results
            with st.expander("View Individual Posts"):
                for r in results:
                    st.markdown(f"### Post {r['post_number']}: {r['topic']}")
                    st.text_area(
                        f"Content (Score: {r['score']:.1f})",
                        r["content"],
                        height=200,
                        key=f"batch_{r['post_number']}"
                    )
                    st.divider()
                    
        except Exception as e:
            st.error(f"Error during batch processing: {e}")


def content_history_ui():
    """Content history interface."""
    st.header("📚 Content History")
    
    if not st.session_state.content_history:
        st.info("No content generated yet. Use the generators to create content!")
        return
        
    # Controls
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Clear History"):
            st.session_state.content_history = []
            st.rerun()
            
    # Display history
    for i, entry in enumerate(st.session_state.content_history):
        metadata = entry["metadata"]
        timestamp = datetime.fromisoformat(entry["timestamp"]).strftime("%Y-%m-%d %H:%M")
        
        with st.expander(
            f"{metadata['type']} - {metadata.get('topic', 'N/A')[:50]} - {timestamp}"
        ):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Score", f"{metadata.get('score', 0):.1f}/10")
            with col2:
                st.metric("Words", metadata.get('word_count', 0))
            with col3:
                st.metric("Lens", metadata.get('lens', 'N/A'))
                
            st.text_area(
                "Content",
                entry["content"],
                height=200,
                key=f"history_{i}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy", key=f"copy_{i}"):
                    st.toast("Content copied!")
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{i}"):
                    st.session_state.content_history.pop(i)
                    st.rerun()


def main():
    """Main application."""
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("✍️ Content Agent System")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            [
                "LinkedIn Generator",
                "Blog Generator",
                "Article Generator",
                "Batch Processor",
                "Content History"
            ]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        AI-powered content generation system with:
        - RAG knowledge base
        - Quality validation (8.0+ threshold)
        - Batch processing
        - Calendar integration
        """)
        
    # Main content
    if page == "LinkedIn Generator":
        linkedin_post_generator()
    elif page == "Blog Generator":
        blog_post_generator()
    elif page == "Article Generator":
        article_generator()
    elif page == "Batch Processor":
        batch_processor_ui()
    elif page == "Content History":
        content_history_ui()


if __name__ == "__main__":
    main()
