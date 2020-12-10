import setuptools

with open("README.md", mode = 'r', encoding = 'utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = "nlingua",
    version = "0.0.1",
    author = "clueless-skywatcher",
    author_email = "somichat@gmail.com",
    description = "An NLP library in Python written from scratch; Inspired by NLTK",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/clueless-skywatcher/nlingua",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = ">=3.4"
)