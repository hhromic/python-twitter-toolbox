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

"""Twitter User-objects module."""

import logging
import json
from os import path
try:
    from itertools import izip_longest as zip_longest  # pylint: disable=no-name-in-module
except ImportError:
    from itertools import zip_longest  # pylint: disable=no-name-in-module
from tweepy import Cursor, TweepError
from .helpers import init_logger, read_config, get_app_auth_api, get_oauth_api
from .helpers import check_and_create_dir

# module constants
LOOKUP_USERS_PER_REQUEST = 100
FOLLOWERS_IDS_COUNT = 5000
FRIENDS_IDS_COUNT = 5000

# module logging
LOGGER = logging.getLogger(__name__)
init_logger(LOGGER)

def _at_least_one(user_ids, screen_names):
    if user_ids is None:
        user_ids = []
    if screen_names is None:
        screen_names = []
    if not user_ids and not screen_names:
        raise ValueError("at least user_ids or screen_names must be provided")
    return user_ids, screen_names

def _only_one(user_id, screen_name):
    if (not user_id and not screen_name) or (user_id and screen_name):
        raise ValueError("only user_id or screen_name must be provided")
    return user_id, screen_name

def _gen_chunks(first, second, size):
    merged = [{"from": "first", "el": el} for el in first] + \
        [{"from": "second", "el": el} for el in second]
    for chunk in zip_longest(*([iter(merged)] * size)):
        yield [el["el"] for el in chunk if el and el["from"] == "first"], \
            [el["el"] for el in chunk if el and el["from"] == "second"]

def _get_ids(writer, endpoint, args, limit=0):
    num_ids = 0
    for user_id in Cursor(endpoint, **args).items(limit):
        writer.write("%d\n" % user_id)
        num_ids += 1
    return num_ids

def _bulk_process(output_dir, filename_tmpl, iterable, function, variable):
    if check_and_create_dir(output_dir):
        LOGGER.info("created output directory: %s", output_dir)
    num_elements = 0
    for element in iterable:
        output_filename = path.join(output_dir, filename_tmpl % element)
        if path.exists(output_filename):
            LOGGER.warning("skipping already processed: %s", element)
            continue
        try:
            LOGGER.info("processing: %d", element)
            with open(output_filename, "w") as writer:
                function(writer, **{variable: element})
            num_elements += 1
        except TweepError:
            LOGGER.exception("exception while using the REST API")
    return num_elements

def get_hydrated(writer, user_ids=None, screen_names=None):
    """Get hydrated Twitter User-objects from a list of user ids and/or screen names."""
    LOGGER.info("get_hydrated() starting")
    user_ids, screen_names = _at_least_one(user_ids, screen_names)

    # initialize config and Twitter API
    config = read_config()
    api = get_oauth_api(config)  # OAuth gives more capacity for the users/lookup API

    # process user ids and/or screen names, storing returned users in JSON format
    num_users = 0
    for chunk in _gen_chunks(user_ids, screen_names, LOOKUP_USERS_PER_REQUEST):
        try:
            for user in api.lookup_users(user_ids=chunk[0], screen_names=chunk[1]):
                writer.write("%s\n" % json.dumps(user._json, separators=(",", ":")))  # pylint: disable=protected-access
                num_users += 1
        except TweepError:
            LOGGER.exception("exception while using the REST API")
    LOGGER.info("downloaded %d user(s)", num_users)

    # finished
    LOGGER.info("get_hydrated() finished")

def get_followers(writer, user_id=None, screen_name=None):
    """Get the ids of the followers for a Twitter user id or screen name."""
    LOGGER.info("get_followers() starting")
    user_id, screen_name = _only_one(user_id, screen_name)

    # initialize config and Twitter API
    config = read_config()
    api = get_app_auth_api(config)

    # process user id or screen name, storing returned ids in plain text
    args = {
        "count": FOLLOWERS_IDS_COUNT,
        "user_id": user_id,
        "screen_name": screen_name,
    }
    result = _get_ids(writer, api.followers_ids, args, config.getint("followers", "limit"))
    LOGGER.info("downloaded %d follower id(s)", result)

    # finished
    LOGGER.info("get_followers() finished")

def bulk_get_followers(output_dir, user_ids=None, screen_names=None):
    """Get the ids of the followers for a bulk of Twitter user ids and/or screen names."""
    LOGGER.info("bulk_get_followers() starting")
    user_ids, screen_names = _at_least_one(user_ids, screen_names)

    # bulk process user ids
    result = _bulk_process(output_dir, "%d.txt", user_ids, get_followers, "user_id")
    if result > 0:
        LOGGER.info("processed %d user ids", result)

    # bulk process screen names
    result = _bulk_process(output_dir, "%s.txt", screen_names, get_followers, "screen_name")
    if result > 0:
        LOGGER.info("processed %d screen names", result)

    # finished
    LOGGER.info("bulk_get_followers() finished")

def get_friends(writer, user_id=None, screen_name=None):
    """Get the ids of the friends for a Twitter user id or screen name."""
    LOGGER.info("get_friends() starting")
    user_id, screen_name = _only_one(user_id, screen_name)

    # initialize config and Twitter API
    config = read_config()
    api = get_app_auth_api(config)

    # process user id or screen name, storing returned ids in plain text
    args = {
        "count": FRIENDS_IDS_COUNT,
        "user_id": user_id,
        "screen_name": screen_name,
    }
    result = _get_ids(writer, api.friends_ids, args, config.getint("friends", "limit"))
    LOGGER.info("downloaded %d friend id(s)", result)

    # finished
    LOGGER.info("get_friends() finished")

def bulk_get_friends(output_dir, user_ids=None, screen_names=None):
    """Get the ids of the friends for a bulk of Twitter user ids and/or screen names."""
    LOGGER.info("bulk_get_friends() starting")
    user_ids, screen_names = _at_least_one(user_ids, screen_names)

    # bulk process user ids
    result = _bulk_process(output_dir, "%d.txt", user_ids, get_friends, "user_id")
    if result > 0:
        LOGGER.info("processed %d user ids", result)

    # bulk process screen names
    result = _bulk_process(output_dir, "%s.txt", screen_names, get_friends, "screen_name")
    if result > 0:
        LOGGER.info("processed %d screen names", result)

    # finished
    LOGGER.info("bulk_get_friends() finished")
