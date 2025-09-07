"""
Setup script for Auto Feedback Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="auto-feedback-generator",
    version="1.0.0",
    author="Adithya",
    description="AI-powered tool to generate personalized feedback for students based on performance rubrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1234-ad/auto-feedback-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-flask>=1.3.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "run-backend=run_backend:main",
            "run-frontend=run_frontend:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml"],
    },
    keywords="education, feedback, ai, nlp, teachers, automation, streamlit, flask",
    project_urls={
        "Bug Reports": "https://github.com/1234-ad/auto-feedback-generator/issues",
        "Source": "https://github.com/1234-ad/auto-feedback-generator",
        "Documentation": "https://github.com/1234-ad/auto-feedback-generator/blob/main/README.md",
    },
)