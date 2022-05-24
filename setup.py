"""Python setup.py for official_website package"""
import io
import os

from setuptools import setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("official_website", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """
    with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    requirements = []
    for line in read(path).split("\n"):
        if line.startswith('.'):
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), line))
            _, package_name = os.path.split(path)
            requirements.append(f"{package_name} @ file://localhost{path}")
        elif line.startswith(('"', "#", "-", "git+")):
            continue
        else:
            requirements.append(line)
    return requirements


setup(
    name="publicNote",
    version=read(".", "VERSION"),
    description="Note some simple idea",
    url="https://github.com/wjshan/publicNote",
    long_description=read("readme.md"),
    long_description_content_type="text/markdown",
    author="wjshan",
    # packages=["mkdocs_jupyter"],
    # package_dir={"mkdocs_jupyter": "plugins/mkdocs_jupyter"},
    install_requires=read_requirements("requirements.txt"),
    # dependency_links=[
    #     # location to your egg file
    #     os.path.join(os.getcwd(), 'plugins/mkdocs_jupyter', 'mkdocs_jupyter.egg-info')
    # ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs_jupyter = plugins.mkdocs_jupyter.plugin:Plugin',
            "mkdocs_last_update = plugins.mkdocs_last_update.plugin:LastModifyAt",
        ]
    },
    extras_require={
        "dev": read_requirements("requirements.dev.txt")
    },
)
