"""
Setup script for singularis-lifeops

Life Operations: Timeline, patterns, interventions, queries.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="singularis-lifeops",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Singularis Life Operations & Timeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/singularis-lifeops",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
    python_requires=">=3.11",
    install_requires=[
        "singularis-core>=1.0.0",  # Core dependency
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "sqlalchemy>=2.0.0",
        "loguru>=0.7.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "postgres": [
            "psycopg2-binary>=2.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lifeops-query=lifeops.cli:query",
            "lifeops-timeline=lifeops.cli:timeline",
        ],
    },
)
