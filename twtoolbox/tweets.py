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
import json
from tweepy import Cursor
from .helpers import init_logger, read_config, get_app_auth_api

# module constants
SEARCH_COUNT = 100

# module logging
LOGGER = logging.getLogger(__name__)
init_logger(LOGGER)

def search(writer, query, since_id=0):
    """Get Tweet-objects from Twitter using the Search API."""
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
    for status in Cursor(api.search, **search_params).items(config.getint("search", "limit")):
        writer.write("%s\n" % json.dumps(status._json, separators=(",", ":")))  # pylint: disable=protected-access
        num_tweets += 1
    LOGGER.info("downloaded %d Tweet(s)", num_tweets)

    # finished
    LOGGER.info("search() finished")
