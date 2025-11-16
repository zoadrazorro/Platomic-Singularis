"""
Setup script for singularis-skyrim

Skyrim AGI environment and control system.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="singularis-skyrim",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Singularis Skyrim AGI Environment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/singularis-skyrim",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=[
        "singularis-core>=1.0.0",
        "singularis-perception>=1.0.0",
        "opencv-python>=4.8.0",
        "pyautogui>=0.9.54",
        "numpy>=1.24.0",
        "loguru>=0.7.0",
        "pydantic>=2.0.0",
        "websockets>=12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "skyrim-agi=skyrim.run_agi:main",
        ],
    },
)
