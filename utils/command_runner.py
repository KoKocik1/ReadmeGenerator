"""Command execution utilities."""

import os
import subprocess
from typing import Optional

from config.settings import Settings

os.chdir(Settings().apps_directory)


class CommandRunner:
    """Utility class for running shell commands."""

    @staticmethod
    def run(command: str, cwd: Optional[str] = None) -> str:
        """
        Run a shell command and return its output.

        Args:
            command: The command to execute.
            cwd: Working directory for the command.

        Returns:
            Command output as a string.

        Raises:
            RuntimeError: If the command fails.
        """

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, check=True, cwd=cwd
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Command failed: {command}\n"
                f"Working directory: {cwd or os.getcwd()}\n"
                f"Error: {e.stderr}"
            )
