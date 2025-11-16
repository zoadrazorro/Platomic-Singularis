"""
Setup script for singularis-integrations

External service adapters (Messenger, Fitbit, cameras, etc.)
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="singularis-integrations",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Singularis External Service Integrations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/singularis-integrations",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications",
        "Topic :: Home Automation",
    ],
    python_requires=">=3.11",
    install_requires=[
        "singularis-core>=1.0.0",
        "singularis-lifeops>=1.0.0",
        "singularis-perception>=1.0.0",
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "aiohttp>=3.8.0",
        "requests>=2.31.0",
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
        "messenger": [
            "facebook-sdk>=3.1.0",
        ],
        "fitbit": [
            "fitbit>=0.3.1",
        ],
        "camera": [
            "opencv-python>=4.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "singularis-orchestrator=integrations.main_orchestrator:main",
        ],
    },
)
