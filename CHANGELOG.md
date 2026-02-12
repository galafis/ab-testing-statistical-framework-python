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

#### Package Infrastructure
- `setup.py` for proper package installation
- Python package structure with `__init__.py` files
- Package metadata and classifiers
- Development dependencies configuration
- Installable via pip in editable mode

#### Documentation
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - MIT License file
- `CHANGELOG.md` - This changelog
- Enhanced README.md with:
  - Testing section
  - Contribution guidelines
  - Installation instructions

### Changed
- Removed unused imports (Tuple, warnings) from ab_test.py
- Updated requirements.txt to include pytest and pytest-cov
- Enhanced README.md with testing and contribution sections

### Fixed
- Code style issues (PEP 8 compliance)
- Removed unused variables in test suite
- Fixed whitespace and indentation inconsistencies

## Code Quality Metrics

- **Test Coverage**: 83%+
- **Total Tests**: 25
- **Code Style**: PEP 8 compliant

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
