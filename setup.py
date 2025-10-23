"""
Setup configuration for A/B Testing Statistical Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ab-testing-statistical-framework",
    version="1.0.0",
    author="Gabriel Demetrios Lafis",
    author_email="",
    description="A comprehensive statistical framework for A/B testing with frequentist and Bayesian approaches",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galafis/ab-testing-statistical-framework-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        'scipy>=1.9.3,<1.11.0; python_version < "3.9"',
        'scipy>=1.11.0; python_version >= "3.9"',
        "numpy>=1.24.0",
        "pandas>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    keywords="ab-testing, statistics, hypothesis-testing, bayesian, frequentist, conversion-rate-optimization",
    project_urls={
        "Bug Reports": "https://github.com/galafis/ab-testing-statistical-framework-python/issues",
        "Source": "https://github.com/galafis/ab-testing-statistical-framework-python",
    },
)
