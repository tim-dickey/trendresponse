# Contributing to TrendResponse

Thank you for your interest in contributing to TrendResponse! We welcome contributions from the community. Here's how to get started:

## Getting Started

1. **Fork the Repository**: Create a personal fork of the TrendResponse repository on GitHub.

2. **Clone Your Fork**: Clone your forked repository to your local machine.

3. **Create a Feature Branch**: Create a feature branch for your work using a descriptive name:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

We maintain consistent code style using the following tools:

### Code Formatting
- **Black**: For Python code formatting
  ```bash
  black src/ tests/
  ```

### Import Sorting
- **isort**: For organizing imports
  ```bash
  isort src/ tests/
  ```

### Linting
- **ruff**: For code quality checks
  ```bash
  ruff check src/ tests/
  ```

Before submitting a pull request, ensure your code passes all these checks:
```bash
black src/ tests/
isort src/ tests/
ruff check src/ tests/
```

## Testing

- Write tests for any new functionality or bug fixes
- Run the test suite using pytest:
  ```bash
  pytest tests/
  ```
- Maintain at least **70% code coverage** for new code
- View coverage report:
  ```bash
  pytest --cov=src tests/
  ```

## Commit Message Format

We follow the **Conventional Commits** format for commit messages. This helps maintain a clear project history and enables automated changelog generation.

### Commit Message Structure
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (formatting, missing semicolons, etc.)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process, dependencies, or other non-code changes

### Examples
```
feat(api): add support for trend analysis

fix(parser): resolve issue with date parsing

docs: update installation instructions

test: add tests for utility functions
```

## Submitting a Pull Request

1. **Push Your Changes**: Push your feature branch to your fork on GitHub.

2. **Create a Pull Request**: Open a pull request from your feature branch to the main TrendResponse repository.

3. **Follow the PR Template**: Complete all sections of the pull request template.

4. **Describe Your Changes**: Provide a clear description of what your pull request does and why.

5. **Link Issues**: If your PR fixes an issue, link it using `Closes #<issue-number>`.

6. **Code Review**: Be prepared to address feedback from maintainers and other contributors.

## Code Review Process

- All pull requests require at least one approval from a maintainer before merging
- Address any requested changes promptly
- Maintain professional and respectful communication

## Questions?

Feel free to open an issue with the label `question` if you have any questions or need clarification on any aspect of contributing.

Thank you for contributing to TrendResponse!
