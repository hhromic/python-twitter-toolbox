#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
  name = "twitter-toolbox",
  packages = find_packages(),
  version = "1.0.dev1",
  description = "Twitter Toolbox for Python",
  long_description = "Twitter Toolbox for Python",
  author = "Hugo Hromic",
  author_email = "hhromic@gmail.com",
  url = "https://github.com/hhromic/python-twitter-toolbox",
  download_url = "https://github.com/hhromic/python-twitter-toolbox/releases/latest",
  install_requires = ["tweepy", "colorlog"],
  keywords = ["twitter", "api", "cli", "toolbox"],
  classifiers = [],
  license = "Apache-2.0",
  platforms = ["all"],
)
