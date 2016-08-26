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
from tweepy import Cursor, TweepError
from .helpers import init_logger, read_config, get_app_auth_api, get_oauth_api
from .helpers import gen_chunks, bulk_process

# module constants
LOOKUP_USERS_PER_REQUEST = 100
FOLLOWERS_IDS_COUNT = 5000
FRIENDS_IDS_COUNT = 5000
SEARCH_COUNT = 20

# module logging
LOGGER = logging.getLogger(__name__)
init_logger(LOGGER)

def _ensure_at_least_one(user_ids, screen_names):
    if user_ids is None:
        user_ids = []
    if screen_names is None:
        screen_names = []
    if not user_ids and not screen_names:
        raise ValueError("at least user_ids or screen_names must be provided")
    return user_ids, screen_names

def _ensure_only_one(user_id, screen_name):
    if (user_id is None and screen_name is None) or \
        (user_id is not None and screen_name is not None):
        raise ValueError("only user_id or screen_name must be provided")
    return user_id, screen_name

def _get_ids(writer, endpoint, args, limit=0):
    num_ids = 0
    for user_id in Cursor(endpoint, **args).items(limit):
        writer.write("%d\n" % user_id)
        num_ids += 1
    return num_ids

def get_hydrated(writer, user_ids=None, screen_names=None):
    """Get hydrated Twitter User-objects from a list of user ids and/or screen names."""
    LOGGER.info("get_hydrated() starting")
    user_ids, screen_names = _ensure_at_least_one(user_ids, screen_names)

    # initialize config and Twitter API
    config = read_config()
    api = get_oauth_api(config)  # OAuth gives more capacity for the users/lookup API

    # process user ids and/or screen names, storing returned users in JSON format
    num_users = 0
    for chunk in gen_chunks(user_ids, screen_names, size=LOOKUP_USERS_PER_REQUEST):
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
    user_id, screen_name = _ensure_only_one(user_id, screen_name)

    # initialize config and Twitter API
    config = read_config()
    api = get_app_auth_api(config)

    # process user id or screen name, storing returned ids in plain text
    args = {"count": FOLLOWERS_IDS_COUNT}
    if user_id is not None:
        args.update({"user_id": user_id})
    if screen_name is not None:
        args.update({"screen_name": screen_name})
    limit = config.getint("followers", "limit")
    result = _get_ids(writer, api.followers_ids, args, limit)
    LOGGER.info("downloaded %d follower id(s)", result)

    # finished
    LOGGER.info("get_followers() finished")

def bulk_get_followers(output_dir, user_ids=None, screen_names=None):
    """Get the ids of the followers for a bulk of Twitter user ids and/or screen names."""
    LOGGER.info("bulk_get_followers() starting")
    user_ids, screen_names = _ensure_at_least_one(user_ids, screen_names)

    # bulk process user ids
    num_processed = bulk_process(LOGGER, output_dir, "%d.txt", get_followers,
                                 [(el, el) for el in user_ids], "user_id")
    if num_processed > 0:
        LOGGER.info("processed %d user ids", num_processed)

    # bulk process screen names
    num_processed = bulk_process(LOGGER, output_dir, "%s.txt", get_followers,
                                 [(el.lower(), el) for el in screen_names], "screen_name")
    if num_processed > 0:
        LOGGER.info("processed %d screen names", num_processed)

    # finished
    LOGGER.info("bulk_get_followers() finished")

def get_friends(writer, user_id=None, screen_name=None):
    """Get the ids of the friends for a Twitter user id or screen name."""
    LOGGER.info("get_friends() starting")
    user_id, screen_name = _ensure_only_one(user_id, screen_name)

    # initialize config and Twitter API
    config = read_config()
    api = get_app_auth_api(config)

    # process user id or screen name, storing returned ids in plain text
    args = {"count": FRIENDS_IDS_COUNT}
    if user_id is not None:
        args.update({"user_id": user_id})
    if screen_name is not None:
        args.update({"screen_name": screen_name})
    limit = config.getint("friends", "limit")
    result = _get_ids(writer, api.friends_ids, args, limit)
    LOGGER.info("downloaded %d friend id(s)", result)

    # finished
    LOGGER.info("get_friends() finished")

def bulk_get_friends(output_dir, user_ids=None, screen_names=None):
    """Get the ids of the friends for a bulk of Twitter user ids and/or screen names."""
    LOGGER.info("bulk_get_friends() starting")
    user_ids, screen_names = _ensure_at_least_one(user_ids, screen_names)

    # bulk process user ids
    num_processed = bulk_process(LOGGER, output_dir, "%d.txt", get_friends,
                                 [(el, el) for el in user_ids], "user_id")
    if num_processed > 0:
        LOGGER.info("processed %d user ids", num_processed)

    # bulk process screen names
    num_processed = bulk_process(LOGGER, output_dir, "%s.txt", get_friends,
                                 [(el.lower(), el) for el in screen_names], "screen_name")
    if num_processed > 0:
        LOGGER.info("processed %d screen names", num_processed)

    # finished
    LOGGER.info("bulk_get_friends() finished")

def search(writer, query):
    """Get User-objects from Twitter using the People Search API."""
    LOGGER.info("search() starting")

    # initialize config and Twitter API
    config = read_config()
    api = get_oauth_api(config)  # only OAuth supported for the users/search API

    # process the query, storing returned users in JSON format
    num_users = 0
    search_params = {
        "q": query,
        "count": SEARCH_COUNT,
    }
    limit = config.getint("search_users", "limit")
    for user in Cursor(api.search_users, **search_params).items(limit):
        writer.write("%s\n" % json.dumps(user._json, separators=(",", ":")))  # pylint: disable=protected-access
        num_users += 1
    LOGGER.info("downloaded %d user(s)", num_users)

    # finished
    LOGGER.info("search() finished")

def bulk_search(output_dir, queries):
    """Get User-objects from Twitter using the People Search API for a bulk of queries."""
    LOGGER.info("bulk_search() starting")

    # bulk process queries
    num_processed = bulk_process(LOGGER, output_dir, "%d.json", search,
                                 enumerate(queries), "query")
    if num_processed > 0:
        LOGGER.info("processed %d queries", num_processed)

    # finished
    LOGGER.info("bulk_search() finished")
