"""Main entry point for the README generator."""

from services.ai_service import AIService
from services.file_service import FileService
from services.git_service import GitService
from services.project_service import ProjectService
from config.settings import Settings
import sys
from pathlib import Path
import traceback

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Main function orchestrating the README generation process."""
    try:
        # Initialize configuration
        settings = Settings()

        # Initialize services
        git_service = GitService()
        file_service = FileService()
        ai_service = AIService(settings.openai_api_key)
        project_service = ProjectService(git_service, file_service, ai_service)

        # Execute the main workflow
        project_service.process_all_projects()

        print("\nScript completed successfully.")

    except Exception as e:
        print(f"ERROR: {e}")
        print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
