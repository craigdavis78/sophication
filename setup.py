"""The setup script for the sophication package."""
import setuptools

with open("README.md", "r") as file_reader:
    long_description = file_reader.read()

setuptools.setup(
    name="sophication",
    version="0.0.1",
    author="Craig Davis",
    author_email="craigdavis78@gmail.com",
    description="A simple flash card program",
    long_description=long_description,
    log_description_content="text/markdown",
    url="https://github.com/craigdavis78/sophication",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Typing :: Typed"
    ],
    python_requires='>=3.6'
)
