# ReadmeGenerator

This is a Python project designed to automate the generation of README.md files for other Python projects based on their codebase and project structure. The application parses project files, interprets their content, and generates comprehensive README documentation including usage guides, installation instructions, and API details if applicable.

## Table of Contents
- [Overview](#overview)
- [Usage](#usage)

## Overview
The ReadmeGenerator project simplifies documentation processes for developers by automatically creating detailed README files. It leverages natural language processing to interpret code and comments within a project, structuring a user-friendly README that includes necessary commands, descriptions, and usage examples. The architecture mainly consists of services handling file operations, AI-based content generation, and Git integration to manage project versions and changes.

## Usage
To start the project locally, follow these steps:
1. Ensure you have Poetry installed on your system.
2. From the project root directory, run:
   ```bash
   poetry install
   poetry run python main.py
   ```

This will install all dependencies and start the application, which will then process the Python projects found within the specified directory.

<!-- Last updated: 8824b256bc46122daaacee7a26137afd3f602adf -->