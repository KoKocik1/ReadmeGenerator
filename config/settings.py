import os
from typing import List
from dotenv import load_dotenv


class Settings:
    """Application configuration settings."""

    def __init__(self):
        """Initialize settings from environment variables."""
        load_dotenv()
        self._validate_environment()

    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key."""
        return os.getenv("OPENAI_API_KEY", "")

    @property
    def required_env_vars(self) -> List[str]:
        """Get list of required environment variables."""
        return ["OPENAI_API_KEY"]

    @property
    def excluded_directories(self) -> List[str]:
        """Get list of directories to exclude from search."""
        return ["node_modules", ".git", "__pycache__", ".venv", "venv"]

    @property
    def apps_directory(self) -> str:
        """Get the apps directory name."""
        return os.getenv("PATH_TO_PROJECT")

    def _validate_environment(self) -> None:
        """Validate that all required environment variables are set."""
        missing_vars = [var for var in self.required_env_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
