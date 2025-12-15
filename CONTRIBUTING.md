# Contributing to Helix

First off, thank you for considering contributing to Helix! It's people like you that make specific open-source tools great. We welcome contributions from everyone. 

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open-source project.  In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## Code of Conduct

This project and everyone participating in it is governed by the [Helix Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for Helix. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

- **Use a clear and descriptive title** for the issue to identify the problem.
- **Describe the exact steps which reproduce the problem** in as many details as possible. 
- **Provide specific examples** to demonstrate the steps.
- **Describe the behavior you observed** after following the steps and point out what exactly is the problem with that behavior. 
- **Explain which behavior you expected to see instead** and why. 
- **Include logs.** Helix logs requests via Redis. If possible, provide relevant logs from the dashboard or standard output.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Helix, including completely new features and minor improvements to existing functionality.

- **Use a clear and descriptive title** for the issue to identify the suggestion.
- **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
- **Explain why this enhancement would be useful** to most Helix users.

### Pull Requests

The process is straightforward: 

1.  **Fork** the repo on GitHub.
2.  **Clone** the project to your own machine. 
3.  **Create a new branch** for your work (`git checkout -b feature/amazing-feature`).
4.  **Commit** changes to your own branch.
5.  **Push** your work back up to your fork.
6.  Submit a **Pull Request** so that we can review your changes. 

**IMPORTANT**: Please ensure your PR adheres to the following:
- Follow PEP 8 guidelines for Python code.
- Ensure that the project builds and runs using Docker.
- If you added new functionality, please add tests.

## Development Setup

Helix can be run locally or via Docker.

### Using Docker (Recommended)

```bash
# Clone your fork (replace with your fork URL if contributing)
git clone https://github.com/ashfromsky/Helix.git
cd Helix

# Start services
docker-compose up --build
```

The application will be available at `http://localhost:8080` (or the configured port).

### Local Setup (Without Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ashfromsky/Helix.git
   cd Helix
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

6. **Start the application:**
   ```bash
   python app/main.py
   ```

## Project Structure

```
Helix/
├── app/                  # Main application code
├── templates/            # HTML templates
├── assets/               # Static assets
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker build instructions
├── setup.sh              # Setup script
├── .env.example          # Example environment variables
└── README.md             # Project documentation
```

## Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/) style guide. 
- Use meaningful variable and function names.
- Add docstrings to all functions and classes.
- Keep functions small and focused on a single task.

### HTML/Templates

- Use semantic HTML5 elements.
- Maintain consistent indentation (2 or 4 spaces).
- Keep templates clean and readable. 

### Commit Messages

- Use clear and descriptive commit messages.
- Start with a verb in the imperative mood (e.g., "Add", "Fix", "Update").
- Keep the first line under 50 characters.
- Provide additional details in the body if necessary.

Example: 
```
Add user authentication feature

- Implement login/logout functionality
- Add session management
- Create login template
```

## Testing

Before submitting a pull request, please ensure:

1. **All existing tests pass:**
   ```bash
   python -m pytest
   ```

2. **New features include tests** where applicable.

3. **The application runs without errors** in Docker: 
   ```bash
   docker-compose up --build
   ```

## Getting Help

If you have questions or need help: 

- Open an [issue](https://github.com/ashfromsky/Helix/issues) on GitHub.
- Check existing issues and discussions for similar questions. 

## License

By contributing to Helix, you agree that your contributions will be licensed under the [GNU Affero General Public License v3.0](LICENSE).

---

Thank you for contributing to Helix! 🚀