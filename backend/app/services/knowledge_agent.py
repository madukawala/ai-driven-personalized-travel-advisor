"""
Knowledge Agent: Retrieves travel knowledge from RAG system
- Searches vector database for relevant travel information
- Performs sentiment scoring
- Returns top-k results with relevance scores
"""

from typing import List, Dict, Any, Optional
import logging
from ..rag.vector_store import VectorStore
from ..utils.config import settings

logger = logging.getLogger(__name__)


class KnowledgeAgent:
    """Agent responsible for retrieving travel knowledge from RAG"""

    def __init__(self, vector_store: VectorStore = None):
        """
        Initialize knowledge agent

        Args:
            vector_store: Optional pre-initialized vector store
        """
        self.vector_store = vector_store or VectorStore()
        self.max_results = settings.MAX_RETRIEVAL_RESULTS
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD

    async def retrieve_knowledge(
        self,
        query: str,
        location: Optional[str] = None,
        activity_type: Optional[str] = None,
        user_interests: Optional[List[str]] = None,
        top_k: int = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant travel knowledge based on query

        Args:
            query: Search query
            location: Optional location filter
            activity_type: Optional activity type filter
            user_interests: Optional user interests for personalization
            top_k: Number of results to return

        Returns:
            List of relevant knowledge snippets with scores
        """
        try:
            # Enhance query with context
            enhanced_query = self._enhance_query(
                query, location, activity_type, user_interests
            )

            # Search vector store
            k = top_k or self.max_results
            results = self.vector_store.search(
                enhanced_query,
                k=k * 2,  # Get more results for filtering
                score_threshold=self.similarity_threshold,
            )

            # Filter and rank results
            filtered_results = self._filter_results(
                results, location, activity_type, user_interests
            )

            # Add sentiment scores
            scored_results = self._add_sentiment_scores(filtered_results)

            # Return top-k results
            return scored_results[:k]

        except Exception as e:
            logger.error(f"Error retrieving knowledge: {e}")
            return []

    def _enhance_query(
        self,
        query: str,
        location: Optional[str],
        activity_type: Optional[str],
        user_interests: Optional[List[str]],
    ) -> str:
        """
        Enhance query with additional context for better retrieval
        """
        enhanced_parts = [query]

        if location:
            enhanced_parts.append(f"in {location}")

        if activity_type:
            enhanced_parts.append(f"related to {activity_type}")

        if user_interests:
            interests_str = ", ".join(user_interests[:3])  # Limit to top 3
            enhanced_parts.append(f"focusing on {interests_str}")

        return " ".join(enhanced_parts)

    def _filter_results(
        self,
        results: List[Dict[str, Any]],
        location: Optional[str],
        activity_type: Optional[str],
        user_interests: Optional[List[str]],
    ) -> List[Dict[str, Any]]:
        """
        Filter results based on metadata and user preferences
        """
        filtered = []

        for result in results:
            # Location filtering
            if location:
                result_locations = result.get("locations", [])
                result_destination = result.get("destination", "").lower()

                if not (
                    location.lower() in result_destination
                    or any(location.lower() in loc.lower() for loc in result_locations)
                ):
                    # Location mismatch, but keep if similarity is very high
                    if result.get("similarity_score", 0) < 0.85:
                        continue

            # Activity type filtering
            if activity_type:
                result_categories = result.get("categories", [])
                if result_categories and activity_type.lower() not in [
                    c.lower() for c in result_categories
                ]:
                    # Activity mismatch, but keep if similarity is high
                    if result.get("similarity_score", 0) < 0.80:
                        continue

            filtered.append(result)

        return filtered

    def _add_sentiment_scores(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add sentiment scores to results
        Uses simple keyword-based sentiment for now
        """
        positive_keywords = [
            "amazing",
            "excellent",
            "beautiful",
            "wonderful",
            "great",
            "fantastic",
            "perfect",
            "love",
            "recommend",
            "best",
        ]

        negative_keywords = [
            "terrible",
            "awful",
            "bad",
            "worst",
            "avoid",
            "disappointing",
            "crowded",
            "expensive",
            "overrated",
            "waste",
        ]

        for result in results:
            text = result.get("text", "").lower()

            # Count sentiment keywords
            positive_count = sum(1 for kw in positive_keywords if kw in text)
            negative_count = sum(1 for kw in negative_keywords if kw in text)

            # Calculate sentiment score (-1 to 1)
            total_count = positive_count + negative_count
            if total_count > 0:
                sentiment = (positive_count - negative_count) / total_count
            else:
                sentiment = 0.0

            result["sentiment_score"] = round(sentiment, 2)

            # Determine sentiment label
            if sentiment > 0.3:
                result["sentiment"] = "positive"
            elif sentiment < -0.3:
                result["sentiment"] = "negative"
            else:
                result["sentiment"] = "neutral"

            # Add helpfulness indicator
            result["is_helpful"] = sentiment >= 0

        # Sort by combination of similarity and sentiment
        results.sort(
            key=lambda x: (
                x.get("similarity_score", 0) * 0.7 + (x.get("sentiment_score", 0) + 1) / 2 * 0.3
            ),
            reverse=True,
        )

        return results

    def get_summary(self, results: List[Dict[str, Any]]) -> str:
        """
        Generate a summary from retrieved knowledge
        """
        if not results:
            return "No relevant information found."

        # Extract key insights
        insights = []
        for result in results[:3]:  # Top 3 results
            text = result.get("text", "")
            # Take first 200 characters as snippet
            snippet = text[:200] + "..." if len(text) > 200 else text
            insights.append(snippet)

        summary = "\n\n".join(f"• {insight}" for insight in insights)
        return summary

    def get_tips_and_recommendations(
        self, results: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Extract practical tips and recommendations from results
        """
        tips = []

        # Keywords that indicate tips/recommendations
        tip_indicators = [
            "tip:",
            "recommendation:",
            "suggest",
            "should",
            "best time",
            "avoid",
            "make sure",
            "don't forget",
        ]

        for result in results:
            text = result.get("text", "").lower()

            # Look for sentences containing tip indicators
            sentences = text.split(".")
            for sentence in sentences:
                if any(indicator in sentence for indicator in tip_indicators):
                    tip = sentence.strip().capitalize()
                    if tip and len(tip) > 20:  # Meaningful tips
                        tips.append(tip)

        # Remove duplicates and limit
        unique_tips = list(dict.fromkeys(tips))
        return unique_tips[:5]
