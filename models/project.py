"""Project model and related data structures."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Project:
    """Represents a project with its metadata and files."""

    name: str
    root_path: Path
    pyproject_toml_path: Path
    base_commit: Optional[str] = None
    changed_files: List[str] = None

    def __post_init__(self):
        """Initialize default values after creation."""
        if self.changed_files is None:
            self.changed_files = []

    @property
    def readme_path(self) -> Path:
        """Get the path to the project's README.md file."""
        return self.root_path / "README.md"

    @property
    def has_changes(self) -> bool:
        """Check if the project has any changed files."""
        return len(self.changed_files) > 0
