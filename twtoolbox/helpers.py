# Twitter Toolbox for Python
# Copyright 2016 Hugo Hromic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Twitter Toolbox for Python helper functions."""

import logging
from codecs import getreader
from os import path
try:
    from configparser import ConfigParser  # pylint: disable=import-error
except ImportError:
    from ConfigParser import ConfigParser  # pylint: disable=import-error
import colorlog
from pkg_resources import resource_stream
from tweepy import API, AppAuthHandler, OAuthHandler

# module constants
CONFIG_DEFAULTS = "defaults.cfg"
CONFIG_USER = "~/.twtoolbox.cfg"

def _read_lines(filename):
    if filename is None:
        return []
    with open(filename) as reader:
        return [line.strip() for line in reader if not line.startswith("#")]

def init_logger(logger):
    """Initialize a logger object."""
    colored_handler = colorlog.StreamHandler()
    colored_handler.setFormatter(colorlog.ColoredFormatter( \
        "%(green)s%(asctime)s%(reset)s " + \
        "%(blue)s[%(cyan)s%(name)s%(blue)s]%(reset)s " + \
        "%(bold)s%(levelname)s%(reset)s " + \
        "%(message)s"))
    logger.setLevel(logging.INFO)
    logger.addHandler(colored_handler)

def read_screen_names(filename):
    """Read a list of Twitter screen names from a file."""
    return _read_lines(filename)

def read_user_ids(filename):
    """Read a list of Twitter user ids from a file."""
    return [int(line) for line in _read_lines(filename)]

def read_config():
    """Read default config and overlay user-defined config."""
    config = ConfigParser()
    config.readfp(getreader('ascii')(resource_stream(__name__, CONFIG_DEFAULTS)))  # pylint: disable=deprecated-method
    config.read(path.expanduser(CONFIG_USER))
    return config

def get_app_auth_api(config):
    """Get a Tweepy API object configured using Application-wide Auth."""
    auth = AppAuthHandler(
        config.get("twitter", "consumer_key"),
        config.get("twitter", "consumer_secret"))
    return API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_oauth_api(config):
    """Get a Tweepy API object configured using OAuth."""
    auth = OAuthHandler(
        config.get("twitter", "consumer_key"),
        config.get("twitter", "consumer_secret"))
    auth.set_access_token(
        config.get("twitter", "access_token_key"),
        config.get("twitter", "access_token_secret"))
    return API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
