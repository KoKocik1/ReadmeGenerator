"""AI service for generating README content."""

import json
import openai
from config.prompts import Prompts


class AIService:
    """Service for AI operations."""

    def __init__(self, api_key: str):
        """
        Initialize AI service.

        Args:
            api_key: OpenAI API key.
        """
        openai.api_key = api_key
        self.prompts = Prompts()

    def generate_readme_content(self, file_content: str) -> str:
        """
        Generate README content using AI.

        Args:
            file_content: Concatenated file content.

        Returns:
            Generated markdown content.
        """
        prompt = self._build_prompt(file_content)

        try:
            response = openai.responses.create(
                model="gpt-4-turbo",
                input=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates README.md files. Always respond with valid JSON in the format {\"markdown\": \"your markdown content here\"}."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )

            response_content = response.output_text
            return self._parse_response(response_content)

        except Exception as e:
            raise RuntimeError(f"Error generating README content: {e}")

    def _build_prompt(self, file_content: str) -> str:
        """Build the complete prompt for AI."""
        base_prompt = self.prompts.get_readme_generation_prompt()
        return f"{base_prompt}\n\n{file_content}"

    def _parse_response(self, response_content: str) -> str:
        """Parse AI response and extract markdown content."""
        try:
            result = json.loads(response_content)
            return result.get("markdown", "")
        except json.JSONDecodeError:
            print("Warning: Could not parse JSON response, using raw content")
            return response_content
