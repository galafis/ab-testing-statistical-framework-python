# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-23

### Added

#### Testing Infrastructure
- Comprehensive test suite with 25 unit and integration tests
- Test coverage: 83%+ code coverage
- Pytest configuration with coverage reporting
- Tests for all major functionality:
  - ABTest initialization
  - Sample size calculation
  - Two-proportion z-test
  - Bayesian A/B testing
  - Result printing
  - Edge cases handling
  - End-to-end integration workflows

#### CI/CD Pipeline
- GitHub Actions workflow for automated testing
- Multi-Python version testing (3.8, 3.9, 3.10, 3.11, 3.12)
- Automated code quality checks with flake8, black, and isort
- Package installation verification
- Test badge in README for build status visibility
- Secure workflow permissions configuration

#### Package Infrastructure
- `setup.py` for proper package installation
- Python package structure with `__init__.py` files
- Package metadata and classifiers
- Development dependencies configuration
- Installable via pip in editable mode

#### Documentation
- `CONTRIBUTING.md` - Comprehensive contribution guidelines
- `LICENSE` - MIT License file
- `CHANGELOG.md` - This changelog
- Enhanced README.md with:
  - CI/CD badge
  - Testing section
  - Contribution guidelines
  - Installation instructions

#### Development Tools
- `.gitignore` - Python-specific ignore patterns
- Code formatting with Black (100 char line length)
- Import sorting with isort
- Linting with flake8

### Changed
- Reformatted entire codebase with Black for consistency
- Removed unused imports (Tuple, warnings) from ab_test.py
- Updated requirements.txt to include pytest and pytest-cov
- Enhanced README.md with testing and contribution sections

### Fixed
- Code style issues (PEP 8 compliance)
- Removed unused variables in test suite
- Fixed whitespace and indentation inconsistencies
- Security: Added explicit permissions to GitHub Actions workflows

### Security
- All CodeQL security checks passed
- No vulnerabilities detected in codebase
- Secure GitHub Actions workflow configuration
- Minimal GITHUB_TOKEN permissions set

## Code Quality Metrics

- **Test Coverage**: 83%+
- **Total Tests**: 25
- **Python Versions Supported**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Security Issues**: 0
- **Code Style**: PEP 8 compliant (via Black)

## Testing Summary

All tests passing (25/25):
- ✅ Initialization tests (2)
- ✅ Sample size calculation tests (4)
- ✅ Two-proportion z-test tests (6)
- ✅ Bayesian A/B test tests (5)
- ✅ Print results tests (2)
- ✅ Edge cases tests (4)
- ✅ Integration tests (2)

[1.0.0]: https://github.com/galafis/ab-testing-statistical-framework-python/releases/tag/v1.0.0
