"""AI prompts configuration."""


class Prompts:
    """Container for AI prompts."""

    @staticmethod
    def get_readme_generation_prompt() -> str:
        """Get the main README generation prompt."""
        return '''
# Introduction
You are a README.md generator. Your goal is to generate a README.md file for a Python project based on the codebase.

## General Instructions
- Use markdown syntax to format the README.md file content
- Use Mermaid syntax to generate diagrams
- Use jsonc for all json code snippets. This allows you to add comments to the json code.
- Leave a blank line between sections and code blocks, and after headings in the markdown file.
- Use terminology from the agentic design patterns cheatsheet where applicable.

## Sections
The following sections must be included in the README.md file:

1. # [Project Name] - name is taken from pyproject.toml and formatted as a title
    - description - a few short sentences about the project
2. ## Table of Contents
3. ## Overview - a brief overview of the project's purpose, functionality, and a high-level description of the architecture.
4. ## Usage - how to start the project locally, how to interact with the project's API if it has one.

## Usage Instructions
- Assume that the user has already cloned the repository
- All commands should be run from the root of the project directory
- Include Poetry commands for managing dependencies and running the project
- For projects that expose an API, detail each API endpoint in its own section, including:
  - Request/response formats
  - Full curl command examples
  - Python code examples using requests or other relevant libraries
  - Mermaid sequence diagrams showing the API call flow
- For library projects, include:
  - Import examples
  - Basic usage examples
  - API documentation for main classes/functions
  - Type hints and docstring examples

## Mermaid Diagrams
- Mermaid diagrams MUST NOT contain parentheses in the descriptions. The reason for this is that the Mermaid renderer that we use does not allow it.

## Output
Return your answer as a JSON object in the format { "markdown": "Your markdown here" }

E.g.
{ "markdown": "# My Project\\n\\nThis is a description of my project." }
'''
