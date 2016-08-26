# Twitter Toolbox for Python

## Installation

You can simply use `pip` (or any similar package manager) for installation:

    $ pip install twitter-toolbox

or, if you prefer a local user installation:

    $ pip install --user twitter-toolbox

## Tools for Tweets

* tt-tweets-get-hydrated
* tt-tweets-get-retweets
* tt-tweets-get-timeline (resumable)
* tt-tweets-search (resumable)

## Tools for Twitter Users

* tt-users-get-hydrated
* tt-users-get-followers
* tt-users-get-friends
* tt-users-search

## Toolbox API

### Tweets

* get_hydrated(writer, tweet_ids)
* get_retweets(writer, tweet_id)
* get_timeline(writer, user_id=None, screen_name=None, since_id=0)
* search(writer, query, since_id=0)
* bulk_get_retweets(output_dir, tweet_ids)
* bulk_get_timeline(output_dir, user_ids=None, screen_names=None)
* bulk_search(output_dir, queries)

### Users

* get_hydrated(writer, user_ids=None, screen_names=None)
* get_followers(writer, user_id=None, screen_name=None)
* get_friends(writer, user_id=None, screen_name=None)
* search(writer, query)
* bulk_get_followers(output_dir, user_ids=None, screen_names=None)
* bulk_get_friends(output_dir, user_ids=None, screen_names=None)
* bulk_search(output_dir, queries)

## License

This software is under the **Apache License 2.0**.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
