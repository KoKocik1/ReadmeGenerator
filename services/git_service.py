"""Git operations service."""

from typing import List, Optional
from pathlib import Path
from utils.command_runner import CommandRunner


class GitService:
    """Service for Git operations."""

    def __init__(self):
        """Initialize Git service."""
        self.command_runner = CommandRunner()

    def get_current_commit_sha(self) -> str:
        """Get the current commit SHA."""
        return self.command_runner.run("git rev-parse HEAD")

    def get_changed_files(
        self, project_root: Path, base_commit: Optional[str] = None
    ) -> List[str]:
        """
        Get list of changed files for a project.

        Args:
            project_root: Root directory of the project.
            base_commit: Base commit to compare against.

        Returns:
            List of changed file paths.
        """
        if base_commit:
            return self._get_diff_files(project_root, base_commit)
        else:
            return self._get_all_tracked_files(project_root)

    def _get_diff_files(self, project_root: Path, base_commit: str) -> List[str]:
        """Get files changed since base commit."""
        try:
            command = f'git diff --name-only {base_commit} HEAD -- "{project_root}"'
            output = self.command_runner.run(command)
            return self._parse_file_list(output)
        except RuntimeError:
            print(
                f"Error getting diff for {project_root}. Falling back to all tracked files."
            )
            return self._get_all_tracked_files(project_root)

    def _get_all_tracked_files(self, project_root: Path) -> List[str]:
        """Get all tracked files in project."""
        command = f'git ls-files "{project_root}"'
        output = self.command_runner.run(command)
        return self._parse_file_list(output)

    def _parse_file_list(self, output: str) -> List[str]:
        """Parse command output into list of file paths."""
        if not output:
            return []
        return [f.strip() for f in output.split("\n") if f.strip()]
