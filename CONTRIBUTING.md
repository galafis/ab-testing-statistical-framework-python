# Contributing to A/B Testing Statistical Framework

First off, thank you for considering contributing to this A/B testing framework! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Be kind and constructive in your communications.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include Python version and OS information**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain the behavior you expected to see**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the [Python style guidelines](#style-guidelines)
* Include appropriate test cases
* Update documentation as needed
* Ensure all tests pass

## Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/ab-testing-statistical-framework-python.git
cd ab-testing-statistical-framework-python
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
pip install -e .  # Install package in editable mode
```

4. **Create a new branch for your feature or bugfix**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

## Testing

We use `pytest` for testing. All contributions should include appropriate tests.

**Run all tests:**

```bash
pytest tests/ -v
```

**Run tests with coverage:**

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

**Run a specific test file:**

```bash
pytest tests/test_ab_framework.py -v
```

**Run a specific test:**

```bash
pytest tests/test_ab_framework.py::TestClassName::test_method_name -v
```

### Writing Tests

* Write tests for any new functionality
* Ensure all tests pass before submitting a PR
* Aim for high test coverage (>80%)
* Use descriptive test names that explain what is being tested
* Follow the existing test structure and naming conventions

## Style Guidelines

### Python Style Guide

We follow PEP 8 with some flexibility:

* **Line length**: Prefer 100 characters, but 127 is acceptable
* **Imports**: Group and sort imports logically
* **Docstrings**: Use Google-style or NumPy-style docstrings
* **Type hints**: Use type hints where appropriate
* **Comments**: Write clear, concise comments for complex logic

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add Bayesian credible interval visualization

- Implement matplotlib-based plotting function
- Add tests for visualization functionality
- Update README with visualization examples

Closes #123
```

### Python Code Style

**Good:**
```python
def calculate_sample_size(
    baseline_rate: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80
) -> int:
    """
    Calculate required sample size for A/B test.
    
    Parameters:
    -----------
    baseline_rate : float
        Current conversion rate (between 0 and 1)
    mde : float
        Minimum detectable effect (relative change)
    alpha : float, optional
        Significance level (default: 0.05)
    power : float, optional
        Statistical power (default: 0.80)
    
    Returns:
    --------
    int
        Required sample size per group
    """
    # Implementation
    pass
```

## Recognition

Contributors will be recognized in the project README. Thank you for your contributions!

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

---

**Happy Contributing!** 🚀
