#!/usr/bin/env python

"""Main setup script."""

from setuptools import setup, find_packages
import twtoolbox.cli

CONSOLE_SCRIPTS = ["%s = twtoolbox.cli:%s" % (fn.replace("_", "-"), fn)
                   for fn in dir(twtoolbox.cli) if fn.startswith("tt_")]

setup(
    name="twitter-toolbox",
    packages=find_packages(),
    version="1.0.0.dev1",
    description="Twitter Toolbox for Python",
    long_description="Twitter Toolbox for Python",
    author="Hugo Hromic",
    author_email="hhromic@gmail.com",
    url="https://github.com/hhromic/python-twitter-toolbox",
    download_url="https://github.com/hhromic/python-twitter-toolbox/releases/latest",
    install_requires=["tweepy", "colorlog"],
    keywords=["twitter", "api", "cli", "toolbox"],
    classifiers=["Environment :: Console"],
    license="Apache-2.0",
    platforms=["all"],
    entry_points={"console_scripts": CONSOLE_SCRIPTS},
)
