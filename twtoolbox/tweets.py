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

"""Twitter Tweet-objects module."""

import logging
from tweepy import TweepError
from .helpers import init_logger, read_config, get_app_auth_api, get_oauth_api
from .helpers import ensure_at_least_one, ensure_only_one, gen_chunks, bulk_process
from .helpers import write_objs, log_tweep_error

# module constants
LOOKUP_STATUSES_PER_REQUEST = 100
RETWEETS_COUNT = 100
TIMELINE_COUNT = 200
SEARCH_COUNT = 100

# module logging
LOGGER = logging.getLogger(__name__)
init_logger(LOGGER)

def get_hydrated(writer, tweet_ids):
    """Get hydrated Tweet-objects from a list of Tweet ids."""
    LOGGER.info("get_hydrated() starting")

    # initialize config and Twitter API
    config = read_config()
    api = get_oauth_api(config)  # OAuth gives more capacity for the statuses/lookup API

    # process Tweet ids, storing returned Tweets in JSON format
    num_tweets = 0
    for chunk in gen_chunks(tweet_ids, size=LOOKUP_STATUSES_PER_REQUEST):
        try:
            num_tweets = write_objs(writer, api.statuses_lookup, {"id_": chunk[0]})
        except TweepError as err:
            log_tweep_error(LOGGER, err)
    LOGGER.info("downloaded %d Tweet(s)", num_tweets)

    # finished
    LOGGER.info("get_hydrated() finished")

def get_retweets(writer, tweet_id):
    """Get hydrated Retweet-objects for a given Tweet id."""
    LOGGER.info("get_retweets() starting")

    # initialize config and Twitter API
    config = read_config()
    api = get_app_auth_api(config)

    # process Tweet id, storing returned Retweets in JSON format
    try:
        num_retweets = write_objs(writer, api.retweets, {"id": tweet_id, "count": RETWEETS_COUNT})
        LOGGER.info("downloaded %d Retweet(s)", num_retweets)
    except TweepError as err:
        log_tweep_error(LOGGER, err)

    # finished
    LOGGER.info("get_retweets() finished")

def bulk_get_retweets(output_dir, tweet_ids):
    """Get hydrated Retweet-objects for a bulk of Tweet ids."""
    LOGGER.info("bulk_get_retweets() starting")

    # bulk process Tweet ids
    num_processed = bulk_process(LOGGER, output_dir, "%d.json", get_retweets,
                                 [(el, el) for el in tweet_ids], "tweet_id")
    if num_processed > 0:
        LOGGER.info("processed %d user ids", num_processed)

    # finished
    LOGGER.info("bulk_get_retweets() finished")

def get_timeline(writer, user_id=None, screen_name=None, since_id=0):
    """Get hydrated Tweet-objects from a user timeline."""
    LOGGER.info("get_timeline() starting")
    ensure_only_one(user_id=user_id, screen_name=screen_name)

    # initialize config and Twitter API
    config = read_config()
    api = get_app_auth_api(config)

    # process user id or screen name, storing returned Tweets in JSON format
    num_tweets = 0
    args = {"count": TIMELINE_COUNT}
    if user_id is not None:
        args.update({"user_id": user_id})
    if screen_name is not None:
        args.update({"screen_name": screen_name})
    if since_id > 0:
        args.update({"since_id": since_id})
    limit = config.getint("timeline", "limit")
    try:
        num_tweets = write_objs(writer, api.user_timeline, args, cursored=True, limit=limit)
        LOGGER.info("downloaded %d Tweet(s)", num_tweets)
    except TweepError as err:
        log_tweep_error(LOGGER, err)

    # finished
    LOGGER.info("get_timeline() finished")

def bulk_get_timeline(output_dir, user_ids=None, screen_names=None):
    """Get hydrated Tweet-objects from a bulk of user timelines."""
    LOGGER.info("bulk_get_timeline() starting")
    ensure_at_least_one(user_ids=user_ids, screen_names=screen_names)

    # bulk process user ids
    if user_ids:
        num_processed = bulk_process(LOGGER, output_dir, "%d.txt", get_timeline,
                                     [(el, el) for el in user_ids],
                                     "user_id", resume=True)
        if num_processed > 0:
            LOGGER.info("processed %d user ids", num_processed)

    # bulk process screen names
    if screen_names:
        num_processed = bulk_process(LOGGER, output_dir, "%s.txt", get_timeline,
                                     [(el.lower(), el) for el in screen_names],
                                     "screen_name", resume=True)
        if num_processed > 0:
            LOGGER.info("processed %d screen names", num_processed)

    # finished
    LOGGER.info("bulk_get_timeline() finished")

def search(writer, query, since_id=0):
    """Get hydrated Tweet-objects using the Search API."""
    LOGGER.info("search() starting")

    # initialize config and Twitter API
    config = read_config()
    api = get_app_auth_api(config)

    # process the query, storing returned Tweets in JSON format
    num_tweets = 0
    search_params = {
        "q": query,
        "count": SEARCH_COUNT,
        "result_type": "recent",
    }
    if since_id > 0:
        search_params.update({"since_id": since_id})
    limit = config.getint("search", "limit")
    try:
        num_tweets = write_objs(writer, api.search, search_params,
                                cursored=True, limit=limit)
        LOGGER.info("downloaded %d Tweet(s)", num_tweets)
    except TweepError as err:
        log_tweep_error(LOGGER, err)

    # finished
    LOGGER.info("search() finished")

def bulk_search(output_dir, queries):
    """Get hydrated Tweet-objects using a bulk of Search API queries."""
    LOGGER.info("bulk_search() starting")

    # bulk process queries
    num_processed = bulk_process(LOGGER, output_dir, "%d.json", search,
                                 enumerate(queries), "query", resume=True)
    if num_processed > 0:
        LOGGER.info("processed %d queries", num_processed)

    # finished
    LOGGER.info("bulk_search() finished")
