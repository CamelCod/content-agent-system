"""Batch content processor with calendar integration."""

import json
from datetime import datetime
from typing import Dict, List, Optional

from agents.linkedin_agent import LinkedInAgent
from agents.validator_agent import ValidatorAgent
from core.knowledge_base import KnowledgeBase
from core.config import MIN_SCORE


# Content Calendar: Week 2-4 (Posts 4-12)
CONTENT_CALENDAR = [
    # Week 2: Posts 4-6
    {
        "week": 2,
        "post_number": 4,
        "topic": "Process theater: why most execution plans look impressive but fail",
        "lens": "processes",
        "objective": "diagnose_failure",
        "description": "Expose how process theater creates illusion of progress without results"
    },
    {
        "week": 2,
        "post_number": 5,
        "topic": "Motivation as tax: why organizations that rely on it always underperform",
        "lens": "incentives",
        "objective": "reframe_belief",
        "description": "Reframe motivation from asset to liability"
    },
    {
        "week": 2,
        "post_number": 6,
        "topic": "Metrics optimization: how measuring the wrong thing creates the wrong behavior",
        "lens": "metrics",
        "objective": "translate_complexity",
        "description": "Show second-order effects of metrics on behavior"
    },
    # Week 3: Posts 7-9
    {
        "week": 3,
        "post_number": 7,
        "topic": "Good people in bad systems: why character doesn't overcome constraints",
        "lens": "constraints",
        "objective": "reframe_belief",
        "description": "Challenge belief that people problems are root cause"
    },
    {
        "week": 3,
        "post_number": 8,
        "topic": "3 things that actually change behavior: incentives, constraints, and feedback",
        "lens": "feedback",
        "objective": "operator_insight",
        "description": "Practical framework for behavior change"
    },
    {
        "week": 3,
        "post_number": 9,
        "topic": "Hidden cost of misaligned incentives: why teams work hard but fail",
        "lens": "incentives",
        "objective": "diagnose_failure",
        "description": "Diagnose failure mode from incentive misalignment"
    },
    # Week 4: Posts 10-12
    {
        "week": 4,
        "post_number": 10,
        "topic": "Advisory approach: how to analyze a system from the outside",
        "lens": "narratives",
        "objective": "advisory_perspective",
        "description": "Framework for external analysis"
    },
    {
        "week": 4,
        "post_number": 11,
        "topic": "Optimization without alignment: why efficiency improvements make things worse",
        "lens": "processes",
        "objective": "diagnose_failure",
        "description": "Show how local optimization breaks global systems"
    },
    {
        "week": 4,
        "post_number": 12,
        "topic": "Rational resistance: when teams push back, the system is usually the problem",
        "lens": "constraints",
        "objective": "reframe_belief",
        "description": "Reframe resistance as signal, not noise"
    }
]


class BatchProcessor:
    """Batch processor for generating multiple content pieces."""
    
    def __init__(
        self,
        model: str = None,
        knowledge_base: Optional[KnowledgeBase] = None,
        max_retries: int = 3
    ):
        """Initialize batch processor.
        
        Args:
            model: Model to use for generation
            knowledge_base: Knowledge base for RAG
            max_retries: Maximum generation attempts per post
        """
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.linkedin_agent = LinkedInAgent(model=model, knowledge_base=self.knowledge_base)
        self.validator = ValidatorAgent(model=model)
        self.max_retries = max_retries
        
    def process_single(self, calendar_entry: Dict) -> Dict:
        """Process a single calendar entry.
        
        Args:
            calendar_entry: Calendar entry dict
            
        Returns:
            Dict with generation results
        """
        print(f"\nGenerating Post #{calendar_entry['post_number']}: {calendar_entry['topic']}")
        
        best_content = None
        best_score = 0.0
        best_feedback = ""
        attempts = 0
        
        for attempt in range(self.max_retries):
            attempts += 1
            print(f"  Attempt {attempt + 1}/{self.max_retries}...")
            
            try:
                # Generate content
                content = self.linkedin_agent.generate(
                    topic=calendar_entry["topic"],
                    lens=calendar_entry["lens"],
                    objective=calendar_entry["objective"]
                )
                
                # Validate content
                score, feedback, word_count = self.validator.validate(
                    content=content,
                    content_type="LinkedIn",
                    target_words="150-250"
                )
                
                print(f"  Score: {score:.1f} | Words: {word_count}")
                
                # Keep track of best attempt
                if score > best_score:
                    best_content = content
                    best_score = score
                    best_feedback = feedback
                    
                # Check if passing
                if score >= MIN_SCORE:
                    print(f"  ✓ Passed validation (score: {score:.1f})")
                    break
                else:
                    print(f"  ✗ Failed validation (score: {score:.1f} < {MIN_SCORE})")
                    
            except Exception as e:
                print(f"  Error: {e}")
                continue
                
        # Prepare result
        result = {
            "post_number": calendar_entry["post_number"],
            "week": calendar_entry["week"],
            "topic": calendar_entry["topic"],
            "lens": calendar_entry["lens"],
            "objective": calendar_entry["objective"],
            "content": best_content or "Failed to generate content",
            "score": best_score,
            "feedback": best_feedback,
            "attempts": attempts,
            "passed": best_score >= MIN_SCORE,
            "word_count": len(best_content.split()) if best_content else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
        
    def process_batch(
        self,
        calendar: Optional[List[Dict]] = None,
        start_post: int = 4,
        end_post: int = 12
    ) -> List[Dict]:
        """Process batch of posts from calendar.
        
        Args:
            calendar: Custom calendar or None for default
            start_post: Starting post number (inclusive)
            end_post: Ending post number (inclusive)
            
        Returns:
            List of results for each post
        """
        if calendar is None:
            calendar = CONTENT_CALENDAR
            
        # Filter calendar
        entries = [
            entry for entry in calendar
            if start_post <= entry["post_number"] <= end_post
        ]
        
        print(f"\n{'='*60}")
        print(f"Batch Processing: Posts {start_post}-{end_post} ({len(entries)} posts)")
        print(f"{'='*60}")
        
        results = []
        for entry in entries:
            result = self.process_single(entry)
            results.append(result)
            
        # Summary
        passed = sum(1 for r in results if r["passed"])
        print(f"\n{'='*60}")
        print(f"Batch Complete: {passed}/{len(results)} posts passed validation")
        print(f"{'='*60}\n")
        
        return results
        
    def export_results(self, results: List[Dict], output_file: str = "batch_results.json"):
        """Export batch results to JSON.
        
        Args:
            results: List of result dicts
            output_file: Output filename
        """
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results exported to {output_file}")
        
    def run_week_2_4(self) -> List[Dict]:
        """Run batch processor for Week 2-4 (Posts 4-12).
        
        Returns:
            List of results
        """
        results = self.process_batch(start_post=4, end_post=12)
        self.export_results(results, "week_2_4_results.json")
        return results


def main():
    """Main entry point for batch processing."""
    print("Content Agent Batch Processor")
    print("="*60)
    
    # Initialize processor
    processor = BatchProcessor()
    
    # Run Week 2-4
    results = processor.run_week_2_4()
    
    # Print summary
    for result in results:
        status = "✓ PASSED" if result["passed"] else "✗ FAILED"
        print(f"Post {result['post_number']}: {status} (Score: {result['score']:.1f})")


if __name__ == "__main__":
    main()
