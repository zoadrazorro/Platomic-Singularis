"""
Setup script for singularis-core

Core AGI consciousness and reasoning system.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="singularis-core",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Singularis Core AGI Consciousness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/singularis-core",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "openai>=1.0.0",
        "google-generativeai>=0.3.0",
        "loguru>=0.7.0",
        "pydantic>=2.0.0",
        "numpy>=1.24.0",
        "aiohttp>=3.8.0",
        "asyncio>=3.4.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "singularis-core=singularis.consciousness.cli:main",
        ],
    },
)
