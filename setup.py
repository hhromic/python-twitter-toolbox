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
    entry_points = {
        "console_scripts": [
            "tt-tweets-get-hydrated = twtoolbox.cli:tt_tweets_get_hydrated",
            "tt-tweets-get-retweets = twtoolbox.cli:tt_tweets_get_retweets",
            "tt-tweets-get-timeline = twtoolbox.cli:tt_tweets_get_timeline",
            "tt-tweets-search = twtoolbox.cli:tt_tweets_search",
            "tt-users-get-hydrated = twtoolbox.cli:tt_users_get_hydrated",
            "tt-users-get-followers = twtoolbox.cli:tt_users_get_followers",
            "tt-users-get-friends = twtoolbox.cli:tt_users_get_friends",
            "tt-users-search = twtoolbox.cli:tt_users_search",
        ],
    },
)
