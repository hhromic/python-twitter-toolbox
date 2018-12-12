"""Main setup script."""

import ast
from os import path
from setuptools import setup, find_packages

NAME = "twitter-toolbox"
VERSION = "1.2.4"
DESCRIPTION = "Twitter Toolbox for Python"
AUTHOR = "Hugo Hromic"
AUTHOR_EMAIL = "hhromic@gmail.com"
URL = "https://github.com/hhromic/python-twitter-toolbox"
DOWNLOAD_URL = URL + "/tarball/" + VERSION

def _read_file(filename):
    with open(filename) as reader:
        return reader.read()

def _gen_console_scripts():
    with open(path.join("twtoolbox", "cli.py")) as reader:
        cli_tree = ast.parse(reader.read())
    return ["%s = twtoolbox.cli:%s" % (fn.name.replace("_", "-"), fn.name)
            for fn in cli_tree.body if isinstance(fn, ast.FunctionDef) and
            fn.name.startswith('tt_')]

setup(
    name=NAME, version=VERSION, description=DESCRIPTION,
    author=AUTHOR, author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR, maintainer_email=AUTHOR_EMAIL,
    url=URL, download_url=DOWNLOAD_URL,
    requires=["tweepy", "colorlog"],
    install_requires=["tweepy", "colorlog"],
    provides=["twtoolbox"],
    keywords=["twitter", "api", "cli", "toolbox"],
    classifiers=["Environment :: Console"],
    license="Apache-2.0",
    platforms=["all"],
    long_description=_read_file("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"twtoolbox": ["defaults.cfg"]},
    entry_points={"console_scripts": _gen_console_scripts()},
)
