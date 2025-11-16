"""
Setup script for singularis-perception

Vision, audio, and multimodal processing.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="singularis-perception",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Singularis Perception (Vision & Audio)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/singularis-perception",
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
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    python_requires=">=3.11",
    install_requires=[
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
        "google-generativeai>=0.3.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "pygame-ce>=2.4.0",
        "numpy>=1.24.0",
        "loguru>=0.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "audio": [
            "pyaudio>=0.2.13",
            "librosa>=0.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "singularis-vision=perception.cli:vision",
        ],
    },
)
