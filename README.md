# Twitter Toolbox for Python

[TODO] summary here.

## Installation

You can simply use `pip` (or any similar package manager) for installation:

    $ pip install twitter-toolbox

or, if you prefer a local user installation:

    $ pip install --user twitter-toolbox

## Configuration File

[TODO] describe the config file.

## Tools for the Streaming API

* `tt-streaming-get-sample`
* `tt-streaming-get-filter`
* `tt-streaming-get-firehose`

All tools have an `--output-file` argument. If omitted, the standard output is used.

Example usage:

    $ tt-streaming-get-sample --output-file tweets.json
    $ tt-streaming-get-filter --track obama trump --follow 6456345
    $ tt-streaming-get-filter --locations -122.75 36.8 -121.75 37.8 -74 40 -73 41
    $ tt-streaming-get-firehose

## Tools for Tweets

* `tt-tweets-get-hydrated`
* `tt-tweets-get-retweets`
* `tt-tweets-get-timeline`
* `tt-tweets-search`

All tools have an `--output-file` argument. If omitted, the standard output is used.

Example usage:

    $ tt-tweets-get-hydrated --tweet-ids tweet_ids.txt --output-file tweets.json
    $ tt-tweets-get-retweets --tweet-id 64563457564
    $ tt-tweets-get-timeline --screen-name insight_centre
    $ tt-tweets-search --query "twitter api"

## Tools for Twitter Users

* `tt-users-get-hydrated`
* `tt-users-get-followers`
* `tt-users-get-friends`
* `tt-users-search`

All tools have an `--output-file` argument. If omitted, the standard output is used.

Example usage:

    $ tt-users-get-hydrated --user-ids user_ids.txt --screen-names screen_names.txt
    $ tt-users-get-followers --user-id 54252345
    $ tt-users-get-friends --screen-name insight_centre
    $ tt-users-search --query "rte" --output-file users.json

## Tools for Bulk Processing

* `tt-tweets-bulk-get-retweets`
* `tt-tweets-bulk-get-timeline`
* `tt-tweets-bulk-search`
* `tt-users-bulk-get-followers`
* `tt-users-bulk-get-friends`
* `tt-users-bulk-search`

All tools have an `--output-dir` argument. The directory is automatically created if not found. Some tools support resuming the bulk processing according to existing files in the output directory.

Example usage:

    $ tt-tweets-bulk-get-retweets --output-dir retweets --tweet-ids tweet_ids.txt
    $ tt-tweets-bulk-get-timeline --output-dir timelines --screen-names screen_names.txt
    $ tt-tweets-bulk-search --output-dir searches --queries queries.txt
    $ tt-users-bulk-get-followers --output-dir followers --user-ids user_ids.txt
    $ tt-users-bulk-get-friends --output-dir friends --screen_names screen_names.txt
    $ tt-users-bulk-search --output-dir searches --queries queries.txt

## Toolbox API

The Twitter toolbox is contained in the `twtoolbox` module. The above command-line tools are actually wrappers around the functions listed below. The same semantics are used, including reading the configuration file.

### Streaming API

The following functions are available in the `streaming` submodule:

* `get_sample(writer)`
* `get_filter(writer, follow=None, track=None, locations=None)`
* `get_firehose(writer)`

Example usage:

```python
from twtoolbox import streaming

with open("tweets.json", "w") as writer:
    streaming.filter(writer, track=["obama"])
```

### Tweets

The following functions are available in the `tweets` submodule:

* `get_hydrated(writer, tweet_ids)`
* `get_retweets(writer, tweet_id)`
* `get_timeline(writer, user_id=None, screen_name=None, since_id=0)`
* `search(writer, query, since_id=0)`
* `bulk_get_retweets(output_dir, tweet_ids)`
* `bulk_get_timeline(output_dir, user_ids=None, screen_names=None)`
* `bulk_search(output_dir, queries)`

Example usage:

```python
from twtoolbox import tweets

with open("tweets.json", "w") as writer:
    tweets.search(writer, query="twitter api")

tweets.bulk_get_retweets("retweets", [768585599271993344, 768585794458120192])
```

### Users

The following functions are available in the `users` submodule:

* `get_hydrated(writer, user_ids=None, screen_names=None)`
* `get_followers(writer, user_id=None, screen_name=None)`
* `get_friends(writer, user_id=None, screen_name=None)`
* `search(writer, query)`
* `bulk_get_followers(output_dir, user_ids=None, screen_names=None)`
* `bulk_get_friends(output_dir, user_ids=None, screen_names=None)`
* `bulk_search(output_dir, queries)`

Example usage:

```python
from twtoolbox import users

with open("followers.txt", "w") as writer:
    users.get_followers(writer, screen_name="twitter")

users.bulk_get_friends("friends", user_ids=[1635345, 645648754])
```

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
