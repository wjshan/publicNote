"""Python setup.py for official_website package"""
import io
import os

from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("official_website", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="publicNote",
    version=read("VERSION"),
    description="Note some simple idea",
    url="https://github.com/wjshan/publicNote",
    long_description=read("readme.md"),
    long_description_content_type="text/markdown",
    author="wjshan",
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        'mkdocs.plugins': [
            'mkdocs_jupyter = plugins.mkdocs_jupyter.plugin:Plugin',
        ]
    },
    extras_require={
        "dev": read_requirements("requirements.dev.txt")
    },
)
