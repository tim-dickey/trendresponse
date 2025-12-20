"""AI-powered comment suggestion service."""

import re
from typing import List

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from src.config import get_settings

settings = get_settings()


class CommentSuggestionService:
    """Service for generating AI-powered comment suggestions."""

    def __init__(self):
        """Initialize the comment suggestion service with GitHub models."""
        self.client = ChatCompletionsClient(
            endpoint=settings.model_endpoint,
            credential=AzureKeyCredential(settings.github_token),
        )
        self.model = settings.model_name
        self.min_words = settings.min_word_count
        self.max_words = settings.max_word_count

    def count_words(self, text: str) -> int:
        """Count words in text.

        Args:
            text: Input text to count words from

        Returns:
            Number of words (whitespace-separated tokens)
        """
        # Remove extra whitespace and split
        words = text.strip().split()
        return len(words)

    def validate_comment(self, comment: str) -> tuple[bool, str]:
        """Validate comment word count.

        Args:
            comment: Comment text to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        word_count = self.count_words(comment)

        if word_count < self.min_words:
            return False, f"Comment must be at least {self.min_words} words (currently {word_count})"
        if word_count > self.max_words:
            return False, f"Comment must be at most {self.max_words} words (currently {word_count})"

        return True, ""

    async def generate_suggestions(
        self, post_content: str, post_author: str, num_suggestions: int = 3
    ) -> List[str]:
        """Generate AI-powered comment suggestions.

        Args:
            post_content: Content of the social media post
            post_author: Author of the post
            num_suggestions: Number of suggestions to generate

        Returns:
            List of suggested comments (10-25 words each)
        """
        system_prompt = f"""You are a helpful assistant that generates concise, professional social media comments.

RULES:
1. Each comment must be EXACTLY between {self.min_words} and {self.max_words} words
2. Be professional, engaging, and add value to the conversation
3. Avoid generic phrases like "Great post!" or "Thanks for sharing!"
4. Provide thoughtful insights, questions, or relevant experiences
5. Match the tone of the original post (professional, casual, technical, etc.)
6. Do NOT use hashtags or excessive emojis

Generate {num_suggestions} different comment suggestions."""

        user_prompt = f"""Generate {num_suggestions} concise comments (10-25 words each) for this social media post:

Author: {post_author}
Post: {post_content}

Format: Return ONLY the comments, one per line, numbered 1. 2. 3. etc."""

        try:
            response = self.client.complete(
                messages=[
                    SystemMessage(system_prompt),
                    UserMessage(user_prompt),
                ],
                temperature=0.8,
                top_p=0.9,
                max_tokens=500,
                model=self.model,
            )

            content = response.choices[0].message.content

            # Parse suggestions from numbered list
            suggestions = []
            lines = content.strip().split("\n")

            for line in lines:
                # Remove numbering (1. 2. 3. etc.) and clean up
                cleaned = re.sub(r"^\d+\.\s*", "", line).strip()
                if cleaned and len(cleaned) > 0:
                    # Validate word count
                    word_count = self.count_words(cleaned)
                    if self.min_words <= word_count <= self.max_words:
                        suggestions.append(cleaned)

            # If we didn't get enough valid suggestions, try to extract any text
            if len(suggestions) < num_suggestions:
                # Return what we have, even if it's less than requested
                pass

            return suggestions[:num_suggestions] if suggestions else ["Unable to generate suggestions. Please try again."]

        except Exception as e:
            # Log error and return fallback
            import structlog

            logger = structlog.get_logger(__name__)
            logger.error("Failed to generate comment suggestions", error=str(e))
            return [f"Error generating suggestions: {str(e)}"]


# Singleton instance
suggestion_service = CommentSuggestionService()
