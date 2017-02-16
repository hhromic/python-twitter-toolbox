#!/usr/bin/env python

"""Main setup script."""

import ast
from os import path
from setuptools import setup, find_packages

CLI_TREE = ast.parse(open(path.join("twtoolbox", "cli.py")).read())
CONSOLE_SCRIPTS = ["%s = twtoolbox.cli:%s" % (fn.name.replace("_", "-"), fn.name)
                   for fn in CLI_TREE.body
                   if isinstance(fn, ast.FunctionDef) and fn.name.startswith('tt_')]

setup(
    packages=find_packages(),
    entry_points={"console_scripts": CONSOLE_SCRIPTS},
)
