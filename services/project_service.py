"""Main project processing service."""

from pathlib import Path
from typing import List
from models.project import Project
from services.git_service import GitService
from services.file_service import FileService
from services.ai_service import AIService
from config.settings import Settings


class ProjectService:
    """Service for processing projects."""

    def __init__(self, git_service: GitService, file_service: FileService, ai_service: AIService):
        """
        Initialize project service.

        Args:
            git_service: Git service instance.
            file_service: File service instance.
            ai_service: AI service instance.
        """
        self.git_service = git_service
        self.file_service = file_service
        self.ai_service = ai_service
        self.settings = Settings()

    def process_all_projects(self) -> None:
        """Process all projects in the repository."""
        projects = self.discover_projects()

        if not projects:
            print(
                "No projects found. Make sure package.json files exist in the expected locations.")
            return

        current_commit = self.git_service.get_current_commit_sha()

        for project in projects:
            self.process_single_project(project, current_commit)

    def discover_projects(self) -> List[Project]:
        """
        Discover all projects in the repository.

        Returns:
            List of discovered projects.
        """
        projects = []

        apps_dir = Path.cwd() / self.settings.apps_directory
        # apps_dir = Path(self.settings.apps_directory)

        if not apps_dir.exists():
            print(
                f"Warning: '{self.settings.apps_directory}' directory not found. Searching from current directory.")
            apps_dir = Path.cwd()

        pyproject_toml_files = self.file_service.find_pyproject_toml_files(
            apps_dir)

        for pyproject_toml_path in pyproject_toml_files:
            project = self._create_project_from_pyproject_toml(
                pyproject_toml_path)
            if project:
                projects.append(project)

        return projects

    def process_single_project(self, project: Project, current_commit: str) -> None:
        """
        Process a single project.

        Args:
            project: Project to process.
            current_commit: Current commit SHA.
        """
        print(
            f'\nProcessing project "{project.name}" at "{project.root_path}" ...')

        # Extract base commit from existing README
        project.base_commit = self.file_service.extract_base_commit_from_readme(
            project.readme_path)

        # Get changed files
        changed_files = self.git_service.get_changed_files(
            project.root_path, project.base_commit)
        project.changed_files = self.file_service.filter_project_files(
            project, changed_files)

        # Skip if no changes
        if not project.has_changes:
            print(
                f'No changes detected for project "{project.name}". Skipping update.')
            return

        # Generate and save README
        self._generate_and_save_readme(project, current_commit)

    def _create_project_from_pyproject_toml(self, pyproject_toml_path: Path) -> Project:
        """
        Create a Project instance from pyproject.toml file.

        Args:
            pyproject_toml_path: Path to pyproject.toml file.

        Returns:
            Project instance or None if error.
        """
        package_data = self.file_service.read_pyproject_toml(
            pyproject_toml_path)

        if not package_data or 'project' not in package_data:
            return None

        return Project(
            name=package_data['project']['name'],
            root_path=pyproject_toml_path.parent,
            pyproject_toml_path=pyproject_toml_path
        )

    def _generate_and_save_readme(self, project: Project, current_commit: str) -> None:
        """
        Generate and save README for a project.

        Args:
            project: Project to generate README for.
            current_commit: Current commit SHA.
        """
        # Concatenate file contents
        file_content = self.file_service.concatenate_file_contents(
            project.changed_files)

        # Generate README content
        markdown_content = self.ai_service.generate_readme_content(
            file_content)

        if not markdown_content:
            print(f'Error: No content generated for project "{project.name}"')
            return

        # Add commit tracking comment
        final_content = f"{markdown_content}\n\n<!-- Last updated: {current_commit} -->"

        # Save to file
        try:
            self.file_service.write_file(project.readme_path, final_content)
            print(f"README saved to {project.readme_path}")
        except Exception as e:
            print(f"Error writing README for {project.name}: {e}")
