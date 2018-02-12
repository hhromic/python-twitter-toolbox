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
import json
from codecs import getreader
from os import path, makedirs
try:
    from configparser import ConfigParser  # pylint: disable=import-error
except ImportError:
    from ConfigParser import ConfigParser  # pylint: disable=import-error
try:
    from itertools import izip_longest as zip_longest  # pylint: disable=no-name-in-module
except ImportError:
    from itertools import zip_longest  # pylint: disable=no-name-in-module
from pkg_resources import resource_stream
import colorlog
from tweepy import TweepError, API, AppAuthHandler, OAuthHandler, Cursor

# module constants
CONFIG_DEFAULTS = "defaults.cfg"
CONFIG_USER = "~/.twtoolbox.cfg"

def _get_latest_id(filename):
    latest_id = None
    with open(filename) as reader:
        for line in reader:
            obj = json.loads(line)
            if latest_id is None or obj["id"] > latest_id:
                latest_id = obj["id"]
    return latest_id

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

def gen_basic_config(consumer_key, consumer_secret, access_token_key, access_token_secret):
    """Generate an initial basic config with Twitter API authentication data."""
    config = ConfigParser()
    config.add_section("twitter")
    config.set("twitter", "consumer_key", consumer_key)
    config.set("twitter", "consumer_secret", consumer_secret)
    config.set("twitter", "access_token_key", access_token_key)
    config.set("twitter", "access_token_secret", access_token_secret)
    with open(path.expanduser(CONFIG_USER), "w") as writer:
        config.write(writer)

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

def ensure_at_least_one(**kwargs):
    """Make sure at least one of the given named arguments has data."""
    one_found = False
    for kwarg in kwargs.values():
        if kwarg:
            one_found = True
    if not one_found:
        raise ValueError("at least one must be provided: %s" % ", ".join(kwargs.keys()))

def ensure_only_one(**kwargs):
    """Make sure only one of the given named arguments has data."""
    only_one_found = False
    for kwarg in kwargs.values():
        if kwarg and only_one_found:
            only_one_found = False
            break
        if kwarg:
            only_one_found = True
    if not only_one_found:
        raise ValueError("only one must be provided: %s" % ", ".join(kwargs.keys()))

def gen_chunks(*iterables, **kwargs):
    """Generate sequential components chunks of certain size from n-iterables."""
    size = kwargs.get("size", 10)
    merged = [(idx, el) for idx, iterable in enumerate(iterables) for el in iterable]
    for chunk in zip_longest(*([iter(merged)] * size)):
        components = [[el[1] for el in chunk if el is not None and
                       el[0] == idx] for idx in range(len(iterables))]
        yield tuple(components)

def write_ids(writer, endpoint, args, cursored=False, limit=0):
    """Connect to an endpoint providing ids and write them in plain text format."""
    num_ids = 0
    ids = endpoint(**args) if not cursored else \
          Cursor(endpoint, **args).items(limit)
    for _id in ids:
        writer.write("%d\n" % _id)
        num_ids += 1
    return num_ids

def write_objs(writer, endpoint, args, cursored=False, limit=0):
    """Connect to an endpoint providing Twitter objects and write them in JSON format."""
    num_objs = 0
    objs = endpoint(**args) if not cursored else \
           Cursor(endpoint, **args).items(limit)
    for obj in objs:
        writer.write("%s\n" % json.dumps(obj._json, separators=(",", ":")))  # pylint: disable=protected-access
        num_objs += 1
    return num_objs

def bulk_process(logger, output_dir, filename_tmpl, function, func_input, var_arg, resume=False):  # pylint: disable=too-many-arguments
    """Process a function in bulk using an iterable input and a variable argument."""
    if not path.exists(output_dir):
        makedirs(output_dir)
        logger.info("created output directory: %s", output_dir)
    num_processed = 0
    for basename, value in func_input:
        output_filename = path.join(output_dir, filename_tmpl % basename)

        # check if there is a previous processing and skip or resume it
        latest_id = None
        if path.exists(output_filename):
            if not resume:
                logger.warning("skipping existing file: %s", output_filename)
                continue
            latest_id = _get_latest_id(output_filename)

        # process the input element with the provided function
        try:
            logger.info("processing: %s", value)
            args = {var_arg: value}
            if latest_id is not None:
                args.update({"since_id": latest_id})
                logger.info("latest id processed: %d", latest_id)
            with open(output_filename, "a" if resume else "w") as writer:
                function(writer, **args)
            num_processed += 1
        except TweepError:
            logger.exception("exception while using the REST API")
    return num_processed

def log_tweep_error(logger, tweep_error):
    """Log a TweepError exception."""
    if tweep_error.api_code:
        if tweep_error.api_code == 32:
            logger.error("invalid API authentication tokens")
        elif tweep_error.api_code == 34:
            logger.error("requested object (user, Tweet, etc) not found")
        elif tweep_error.api_code == 64:
            logger.error("your account is suspended and is not permitted")
        elif tweep_error.api_code == 130:
            logger.error("Twitter is currently in over capacity")
        elif tweep_error.api_code == 131:
            logger.error("internal Twitter error occurred")
        elif tweep_error.api_code == 135:
            logger.error("could not authenticate your API tokens")
        elif tweep_error.api_code == 136:
            logger.error("you have been blocked to perform this action")
        elif tweep_error.api_code == 179:
            logger.error("you are not authorized to see this Tweet")
        else:
            logger.error("error while using the REST API: %s", tweep_error)
    else:
        logger.error("error with Twitter: %s", tweep_error)
