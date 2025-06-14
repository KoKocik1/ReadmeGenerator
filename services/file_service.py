"""File operations service."""

import json
import re
import tomli
from pathlib import Path
from typing import List, Optional, Dict, Any
from config.settings import Settings
from models.project import Project


class FileService:
    """Service for file operations."""

    def __init__(self):
        """Initialize file service."""
        self.settings = Settings()

    def find_pyproject_toml_files(self, start_directory: Path) -> List[Path]:
        """
        Find all pyproject.toml files in directory tree.

        Args:
            start_directory: Directory to start search from.

        Returns:
            List of pyproject.toml file paths.
        """
        results = []

        for item in start_directory.rglob("*"):
            if item.name in self.settings.excluded_directories:
                continue
            if item.name == "pyproject.toml" and item.is_file():
                results.append(item)

        return results

    def read_pyproject_toml(
        self, pyproject_toml_path: Path
    ) -> Optional[Dict[str, Any]]:
        """
        Read and parse pyproject.toml file.

        Args:
            pyproject_toml_path: Path to pyproject.toml file.

        Returns:
            Parsed TOML data or None if error.
        """
        try:
            with open(pyproject_toml_path, "rb") as f:
                return tomli.load(f)
        except (tomli.TOMLDecodeError, IOError) as e:
            print(f"Error reading {pyproject_toml_path}: {e}")
            return None

    def extract_base_commit_from_readme(self, readme_path: Path) -> Optional[str]:
        """
        Extract base commit SHA from README.md file.

        Args:
            readme_path: Path to README.md file.

        Returns:
            Commit SHA if found, None otherwise.
        """
        if not readme_path.exists():
            return None

        try:
            content = self.read_file(readme_path)
            match = re.search(
                r"<!--\s*Last\s+updated:\s*([a-f0-9]+)\s*-->", content, re.IGNORECASE
            )
            return match.group(1) if match else None
        except Exception as e:
            print(f"Error extracting base commit from {readme_path}: {e}")
            return None

    def read_file(self, file_path: Path) -> str:
        """
        Read file content as string.

        Args:
            file_path: Path to file.

        Returns:
            File content as string.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, file_path: Path, content: str) -> None:
        """
        Write content to file.

        Args:
            file_path: Path to file.
            content: Content to write.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def filter_project_files(
        self, project: Project, file_paths: List[str]
    ) -> List[str]:
        """
        Filter files to include only those within project root and exclude README.md and poetry.lock.

        Args:
            project: Project instance.
            file_paths: List of file paths to filter.

        Returns:
            Filtered list of file paths.
        """
        filtered_files = []

        for file_path in file_paths:
            path_obj = Path(file_path)

            try:
                # Check if file is within project root
                path_obj.resolve().relative_to(project.root_path.resolve())

                # Exclude README.md and poetry.lock files
                if path_obj.name not in ["README.md", "poetry.lock"]:
                    filtered_files.append(file_path)

            except ValueError:
                # File is not within project root
                continue

        return filtered_files

    def concatenate_file_contents(self, file_paths: List[str]) -> str:
        """
        Concatenate file paths and their contents.

        Args:
            file_paths: List of file paths.

        Returns:
            Concatenated content string.
        """
        content = ""

        for file_path in file_paths:
            path_obj = Path(file_path)

            if not path_obj.exists():
                continue

            content += f"{file_path}\n"

            try:
                file_content = self.read_file(path_obj)
                content += f"{file_content}\n\n"
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue

        return content
