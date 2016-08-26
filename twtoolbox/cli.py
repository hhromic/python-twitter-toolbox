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

from argparse import ArgumentParser
from . import tweets
from . import users

def _read_strings(filename):
    if filename is None:
        return []
    with open(filename) as reader:
        return [line.strip() for line in reader if not line.startswith("#")]

def _read_integers(filename):
    return [int(line) for line in _read_strings(filename)]

def tt_tweets_get_hydrated():
    """Interface to tweets.get_hydrated()"""
    parser = ArgumentParser(description=tweets.get_hydrated.__doc__)
    parser.add_argument("--tweet-ids", metavar="FILE", required=True,
                        help="file with input Tweet ids (text format)")
    parser.add_argument("--output-file", metavar="FILE", required=True,
                        help="file for output hydrated Tweets (JSON format)")
    args = parser.parse_args()
    tweet_ids = _read_integers(args.tweet_ids)
    with open(args.output_file, "w") as writer:
        tweets.get_hydrated(writer, tweet_ids)

def tt_tweets_get_retweets():
    """Interface to tweets.bulk_get_retweets()"""
    parser = ArgumentParser(description=tweets.bulk_get_retweets.__doc__)
    parser.add_argument("--tweet-ids", metavar="FILE", required=True,
                        help="file with input Tweet ids (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output Retweets (JSON format)")
    args = parser.parse_args()
    tweet_ids = _read_integers(args.tweet_ids)
    tweets.bulk_get_retweets(args.output_dir, tweet_ids)

def tt_tweets_get_timeline():
    """Interface to tweets.bulk_get_timeline()"""
    parser = ArgumentParser(description=tweets.bulk_get_timeline.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output Tweets (JSON format)")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    tweets.bulk_get_timeline(args.output_dir, user_ids, screen_names)

def tt_tweets_search():
    """Interface to tweets.bulk_search()"""
    parser = ArgumentParser(description=tweets.bulk_search.__doc__)
    parser.add_argument("--queries", metavar="FILE", required=True,
                        help="file with input queries (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output Tweets (JSON format)")
    args = parser.parse_args()
    queries = _read_strings(args.queries)
    tweets.bulk_search(args.output_dir, queries)

def tt_users_get_hydrated():
    """Interface to users.get_hydrated()"""
    parser = ArgumentParser(description=users.get_hydrated.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-file", metavar="FILE", required=True,
                        help="file for output hydrated users (JSON format)")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    with open(args.output_file, "w") as writer:
        users.get_hydrated(writer, user_ids, screen_names)

def tt_users_get_followers():
    """Interface to users.bulk_get_followers()"""
    parser = ArgumentParser(description=users.bulk_get_followers.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output user ids (text format)")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    users.bulk_get_followers(args.output_dir, user_ids, screen_names)

def tt_users_get_friends():
    """Interface to users.bulk_get_friends()"""
    parser = ArgumentParser(description=users.bulk_get_friends.__doc__)
    parser.add_argument("--user-ids", metavar="FILE",
                        help="file with input user ids (text format)")
    parser.add_argument("--screen-names", metavar="FILE",
                        help="file with input user screen names (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output user ids (text format)")
    args = parser.parse_args()
    user_ids = _read_integers(args.user_ids)
    screen_names = _read_strings(args.screen_names)
    users.bulk_get_friends(args.output_dir, user_ids, screen_names)

def tt_users_search():
    """Interface to users.bulk_search()"""
    parser = ArgumentParser(description=users.bulk_search.__doc__)
    parser.add_argument("--queries", metavar="FILE", required=True,
                        help="file with input queries (text format)")
    parser.add_argument("--output-dir", metavar="DIRECTORY", required=True,
                        help="directory for output users (JSON format)")
    args = parser.parse_args()
    queries = _read_strings(args.queries)
    users.bulk_search(args.output_dir, queries)
