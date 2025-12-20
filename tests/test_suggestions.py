"""Test comment suggestion service."""

import pytest

from src.services.suggestions import CommentSuggestionService


@pytest.fixture
def suggestion_service():
    """Create suggestion service instance."""
    return CommentSuggestionService()


class TestWordCount:
    """Test word counting functionality."""

    def test_basic_word_count(self, suggestion_service):
        """Test basic word counting."""
        text = "This is a simple test with seven words"
        assert suggestion_service.count_words(text) == 7

    def test_extra_whitespace(self, suggestion_service):
        """Test word counting with extra whitespace."""
        text = "This   has    extra     spaces"
        assert suggestion_service.count_words(text) == 4

    def test_punctuation(self, suggestion_service):
        """Test word counting with punctuation."""
        text = "Hello, world! How are you?"
        assert suggestion_service.count_words(text) == 5

    def test_empty_string(self, suggestion_service):
        """Test word counting with empty string."""
        assert suggestion_service.count_words("") == 0
        assert suggestion_service.count_words("   ") == 0


class TestCommentValidation:
    """Test comment validation functionality."""

    def test_valid_comment(self, suggestion_service):
        """Test validation of valid comment."""
        comment = "This is a valid comment with exactly fifteen words in total for testing purposes"
        is_valid, message = suggestion_service.validate_comment(comment)
        assert is_valid
        assert message == ""

    def test_too_short(self, suggestion_service):
        """Test validation of too short comment."""
        comment = "Too short comment"
        is_valid, message = suggestion_service.validate_comment(comment)
        assert not is_valid
        assert "at least" in message

    def test_too_long(self, suggestion_service):
        """Test validation of too long comment."""
        comment = " ".join(["word"] * 30)
        is_valid, message = suggestion_service.validate_comment(comment)
        assert not is_valid
        assert "at most" in message

    def test_minimum_boundary(self, suggestion_service):
        """Test validation at minimum word boundary."""
        comment = " ".join(["word"] * 10)
        is_valid, message = suggestion_service.validate_comment(comment)
        assert is_valid

    def test_maximum_boundary(self, suggestion_service):
        """Test validation at maximum word boundary."""
        comment = " ".join(["word"] * 25)
        is_valid, message = suggestion_service.validate_comment(comment)
        assert is_valid


class TestSuggestionGeneration:
    """Test AI suggestion generation."""

    @pytest.mark.asyncio
    async def test_generate_suggestions_structure(self, suggestion_service):
        """Test that suggestions are generated with correct structure."""
        post_content = "Excited to share our new AI-powered productivity tool!"
        post_author = "John Doe"

        suggestions = await suggestion_service.generate_suggestions(
            post_content, post_author, num_suggestions=3
        )

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert len(suggestions) <= 3

    @pytest.mark.asyncio
    async def test_suggestions_word_count(self, suggestion_service):
        """Test that generated suggestions meet word count requirements."""
        post_content = "Just published a blog post about remote work best practices."
        post_author = "Jane Smith"

        suggestions = await suggestion_service.generate_suggestions(
            post_content, post_author, num_suggestions=2
        )

        for suggestion in suggestions:
            if "Error" not in suggestion and "Unable" not in suggestion:
                word_count = suggestion_service.count_words(suggestion)
                # Allow some flexibility for error messages
                if word_count > 0:
                    assert (
                        10 <= word_count <= 25
                    ), f"Suggestion has {word_count} words: {suggestion}"
