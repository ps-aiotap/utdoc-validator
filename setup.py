from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="utdoc-validator",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to validate unit test documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/utdoc-validator",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/utdoc-validator/issues",
        "Documentation": "https://github.com/yourusername/utdoc-validator#readme",
        "Source Code": "https://github.com/yourusername/utdoc-validator",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.12.0",
            "black>=21.5b2",
            "flake8>=3.9.2",
            "isort>=5.9.1",
            "mypy>=0.812",
            "pre-commit>=2.13.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "utdoc-validator=utdoc_validator.cli:main",
        ],
    },
)