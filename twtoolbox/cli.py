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

"""Command-line Interface module."""

import sys
import logging
from argparse import ArgumentParser
from contextlib import closing
from .helpers import init_logger, gen_basic_config
from . import streaming
from . import tweets
from . import users

try:
    input = raw_input  # pylint: disable=redefined-builtin, invalid-name
except NameError:
    pass

# module logging
LOGGER = logging.getLogger(__name__)
init_logger(LOGGER)

def _get_writer(filename, resume=False):
    if filename is None:
        if "__exit__" in dir(sys.stdout):
            return sys.stdout
        return closing(sys.stdout)
    return open(filename, "a" if resume else "w")

def _read_strings(filename):
    if filename is None:
        return []
    with open(filename) as reader:
        return [line.strip() for line in reader if not line.startswith("##")]

def _read_integers(filename):
    return [int(line) for line in _read_strings(filename)]

def _safe_call(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as excp:  # pylint: disable=broad-except
        LOGGER.error(excp)

### Tools for Configuring the Toolbox ###

def tt_config():
    """Generate a basic config file for the Toolbox using Twitter authentication data."""
    print("WARNING: this tool will create a **NEW** config file and")
    print("  overwrite any existing previous configuration.\n")
    consumer_key = input("Consumer Key ...... : ")
    consumer_secret = input("Consumer Secret ... : ")
    access_token_key = input("Access Token Key .. : ")
    access_token_secret = input("Access Token Secret : ")
    gen_basic_config(consumer_key, consumer_secret, access_token_key, access_token_secret)

### Tools for the Streaming API ###

def tt_streaming_get_sample():
    """Interface to streaming.get_sample()"""
    parser = ArgumentParser(description=streaming.get_sample.__doc__)
    parser.add_argument("--output-file", metavar="FILE", required=False,
                        help="file for output hydrated Tweets (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(streaming.get_sample, writer)

def tt_streaming_get_filter():
    """Interface to streaming.get_filter()"""
    parser = ArgumentParser(description=streaming.get_filter.__doc__)
    parser.add_argument("--follow", metavar="USER_ID", type=int, nargs='+',
                        help="list of user ids to follow")
    parser.add_argument("--track", metavar="TERM", nargs='+',
                        help="list of Twitter terms to track")
    parser.add_argument("--locations", metavar="COORDINATE", type=float, nargs='+',
                        help="list of coordinates to filter by locations")
    parser.add_argument("--output-file", metavar="FILE", required=False,
                        help="file for output hydrated Tweets (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    if args.locations and (len(args.locations) % 4) != 0:
        parser.error("you must give exactly four coordinates per bounding box")
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(streaming.get_filter, writer,
                   follow=args.follow, track=args.track, locations=args.locations)

def tt_streaming_get_firehose():
    """Interface to streaming.firehose()"""
    parser = ArgumentParser(description=streaming.get_firehose.__doc__)
    parser.add_argument("--output-file", metavar="FILE", required=False,
                        help="file for output hydrated Tweets (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(streaming.get_firehose, writer)

### Tools for Tweets ###

def tt_tweets_get_hydrated():
    """Interface to tweets.get_hydrated()"""
    parser = ArgumentParser(description=tweets.get_hydrated.__doc__)
    parser.add_argument("--tweet-ids", metavar="FILE", required=True,
                        help="file with input Tweet ids (text format)")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output hydrated Tweets (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    tweet_ids = _read_integers(args.tweet_ids)
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(tweets.get_hydrated, writer, tweet_ids)

def tt_tweets_get_retweets():
    """Interface to tweets.get_retweets()"""
    parser = ArgumentParser(description=tweets.get_retweets.__doc__)
    parser.add_argument("--tweet-id", metavar="TWEET_ID", type=int, required=True,
                        help="Tweet Id to get the retweets for")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output hydrated Retweets (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(tweets.get_retweets, writer, args.tweet_id)

def tt_tweets_get_timeline():
    """Interface to tweets.get_timeline()"""
    parser = ArgumentParser(description=tweets.get_timeline.__doc__)
    parser.add_argument("--user-id", metavar="USER_ID", type=int,
                        help="User Id to get the timeline for")
    parser.add_argument("--screen-name", metavar="SCREEN_NAME",
                        help="User screen name to get the timeline for")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output hydrated Tweets (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(tweets.get_timeline, writer,
                   user_id=args.user_id, screen_name=args.screen_name)

def tt_tweets_search():
    """Interface to tweets.search()"""
    parser = ArgumentParser(description=tweets.search.__doc__)
    parser.add_argument("--query", metavar="QUERY", required=True,
                        help="query for searching Tweets")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output hydrated Tweets (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(tweets.search, writer, args.query)

### Tools for Twitter Users ###

def tt_users_get_hydrated():
    """Interface to users.get_hydrated()"""
    parser = ArgumentParser(description=users.get_hydrated.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output hydrated users (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(users.get_hydrated, writer, user_ids, screen_names)

def tt_users_get_followers():
    """Interface to users.get_followers()"""
    parser = ArgumentParser(description=users.get_followers.__doc__)
    parser.add_argument("--user-id", metavar="USER_ID", type=int,
                        help="User Id to get the followers for")
    parser.add_argument("--screen-name", metavar="SCREEN_NAME",
                        help="User screen name to get the followers for")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output follower ids (text format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(users.get_followers, writer,
                   user_id=args.user_id, screen_name=args.screen_name)

def tt_users_get_friends():
    """Interface to users.get_friends()"""
    parser = ArgumentParser(description=users.get_friends.__doc__)
    parser.add_argument("--user-id", metavar="USER_ID", type=int,
                        help="User Id to get the friends for")
    parser.add_argument("--screen-name", metavar="SCREEN_NAME",
                        help="User screen name to get the friends for")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output friend ids (text format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(users.get_friends, writer,
                   user_id=args.user_id, screen_name=args.screen_name)

def tt_users_search():
    """Interface to users.search()"""
    parser = ArgumentParser(description=users.search.__doc__)
    parser.add_argument("--query", metavar="QUERY", required=True,
                        help="query for searching users")
    parser.add_argument("--output-file", metavar="FILE",
                        help="file for output hydrated users (JSON format)")
    parser.add_argument("--resume", action="store_true", required=False,
                        help="resume writing to the output file instead of truncating")
    args = parser.parse_args()
    with _get_writer(args.output_file, args.resume) as writer:
        _safe_call(users.search, writer, args.query)

### Tools for Bulk Processing ###

def tt_tweets_bulk_get_retweets():
    """Interface to tweets.bulk_get_retweets()"""
    parser = ArgumentParser(description=tweets.bulk_get_retweets.__doc__)
    parser.add_argument("--tweet-ids", metavar="FILE", required=True,
                        help="file with input Tweet ids (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output hydrated Retweets (JSON format)")
    args = parser.parse_args()
    tweet_ids = _read_integers(args.tweet_ids)
    _safe_call(tweets.bulk_get_retweets, args.output_dir, tweet_ids)

def tt_tweets_bulk_get_timeline():
    """Interface to tweets.bulk_get_timeline()"""
    parser = ArgumentParser(description=tweets.bulk_get_timeline.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output hydrated Tweets (JSON format)")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    _safe_call(tweets.bulk_get_timeline, args.output_dir, user_ids, screen_names)

def tt_tweets_bulk_search():
    """Interface to tweets.bulk_search()"""
    parser = ArgumentParser(description=tweets.bulk_search.__doc__)
    parser.add_argument("--queries", metavar="FILE", required=True,
                        help="file with input queries (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output hydrated Tweets (JSON format)")
    args = parser.parse_args()
    queries = _read_strings(args.queries)
    _safe_call(tweets.bulk_search, args.output_dir, queries)

def tt_users_bulk_get_followers():
    """Interface to users.bulk_get_followers()"""
    parser = ArgumentParser(description=users.bulk_get_followers.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output follower ids (text format)")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    _safe_call(users.bulk_get_followers, args.output_dir, user_ids, screen_names)

def tt_users_bulk_get_friends():
    """Interface to users.bulk_get_friends()"""
    parser = ArgumentParser(description=users.bulk_get_friends.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output friend ids (text format)")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    _safe_call(users.bulk_get_friends, args.output_dir, user_ids, screen_names)

def tt_users_bulk_search():
    """Interface to users.bulk_search()"""
    parser = ArgumentParser(description=users.bulk_search.__doc__)
    parser.add_argument("--queries", metavar="FILE", required=True,
                        help="file with input queries (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output hydrated users (JSON format)")
    args = parser.parse_args()
    queries = _read_strings(args.queries)
    _safe_call(users.bulk_search, args.output_dir, queries)
