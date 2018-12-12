# Twitter Toolbox for Python

Often we need to interact with the [Twitter APIs](https://dev.twitter.com/overview/api) to grab some data for research purposes or simple curiosity.

The Twitter API is very rich and powerful, however for many non-experienced users it can be tedious, cumbersome and tricky to code. Specially if you just want quick and reliable access to the API's methods!

For all those users who just want zero programming, this Twitter Toolbox might be very handy. And for those users that want more programmatic access, this Toolbox is also suitable and helpful!

All you need to do to easily start working with the Twitter APIs is to:

1. Sign-up for your own [Twitter App](https://apps.twitter.com/).
2. Configure the Toolbox with your generated personal access credentials.
3. Use the provided command-line tools.
4. *(optional)* use the provided higher-level Toolbox API for Python in your own code.

Want to grab the list of followers of user `@insight_centre`? No problem:

    tt-users-get-followers --screen-name insight_centre --output-file followers.ids

Want to turn those user Ids into fully hydrated Twitter User objects? No problem:

    tt-users-get-hydrated --user-ids followers.ids --output-file followers.json

Want to receive some real-time Tweets about `obama` or mentioning `@realDonaldTrump`? No problem:

    tt-streaming-get-filter --track obama @realDonaldTrump --output-file tweets.json

Want to see current real-time sample of Tweets text and you have the [`jq` tool](https://stedolan.github.io/jq/) installed? No problem:

    tt-streaming-get-sample | jq .text

As seen, you can omit the `--output-file` argument to get data into your standard output pipe.

Finally, many tools have a **bulk processing** variant that allows you to download data in batches directly and easily. For example if you have a list of user ids stored in a file, you can download the follower ids for each of them in separate files stored under a directory using just one command:

    tt-users-bulk-get-followers --output-dir followers --user-ids user_ids.txt

In case of any errors, simply run the command again and it will resume the bulk processing from where it was left.

## Installation

You can use `pip` (or any `PyPI`-compatible package manager) for installation:

    pip install twitter-toolbox

or, if you prefer a local user installation:

    pip install --user twitter-toolbox

For **Microsoft Windows** users, you might need to run `pip` through the Python interpreter:

    python -m pip install twitter-toolbox

## Configuration File

The Twitter Toolbox is globally configured using the simple [configuration language from Python](https://docs.python.org/2/library/configparser.html) stored into a file named `.twtoolbox.cfg` under your home directory (please note the leading period `.`).

You can easily create a minimal basic configuration from your Twitter API access credentials using the `tt-config` command-line tool. Example usage:

    $ tt-config
    WARNING: this tool will create a **NEW** config file and
      overwrite any existing previous configuration.

    Consumer Key ...... : <INPUT YOUR CONSUMER KEY HERE>
    Consumer Secret ... : <INPUT YOUR CONSUMER SECRET HERE>
    Access Token Key .. : <INPUT YOUR ACCESS TOKEN KEY HERE>
    Access Token Secret : <INPUT YOUR ACCESS TOKEN SECRET HERE>

After you input your authentication data, a new minimal configuration file will be created in your home directory (replacing any previous existing file!).

You can further customize this file using the below configuration sections and options. The available configuration sections and options are:

* `[twitter]`: **(required)** for configuring your own Twitter API's access credentials. Options: `consumer_key`, `consumer_secret`, `access_token_key`, `access_token_secret`.
* `[search]`: for configuring access to the Tweets Search API. Options: `limit`.
* `[search_users]`: for configuring access to the Users Search API. Options: `limit`.
* `[timeline]`: for configuring access to the Users Timeline API. Options: `limit`.
* `[followers]`: for configuring access to the User Followers API. Options: `limit`.
* `[friends]`: for configuring access to the User Friends API. Options: `limit`.
* `[sample]`: for configuring access to the Streaming API's Sample Endpoint. Options: `limit`.
* `[filter]`: for configuring access to the Streaming API's Filter Endpoint. Options: `limit`.
* `[firehose]`: for configuring access to the Streaming API's Firehose Endpoint. Options: `limit`.

All the `limit` options specify the maximum number of results (users, Tweets, Ids) you want to download from Twitter, with `0` meaning *unlimited*. Be very careful with this option, the higher the number the easier you will exhaust your [API rate limits](https://dev.twitter.com/rest/public/rate-limiting). It is strongly recommended that you use the defaults from the Toolbox.

The following is a full example of a suitable configuration file. You can omit those sections/options that you want the defaults to be used. The very minimum is the `[twitter]` section with your configured API credentials.

    [twitter]
    consumer_key=YOUR_CONSUMER_KEY_HERE
    consumer_secret=YOUR_CONSUMER_SECRET_HERE
    access_token_key=YOUR_ACCESS_TOKEN_KEY_HERE
    access_token_secret=YOUR_ACCESS_TOKEN_SECRET_HERE

    [search]
    limit = 0

    [search_users]
    limit = 1000

    [timeline]
    limit = 0

    [followers]
    limit = 30000

    [friends]
    limit = 30000

    [sample]
    limit = 0

    [filter]
    limit = 0

    [firehose]
    limit = 0

The option values under the `[twitter]` section must be replaced by your own **Twitter App credentials**.

If the configuration file, any section or option are not specified, built-in defaults are used.

## Tools for the Streaming API

* `tt-streaming-get-sample`
* `tt-streaming-get-filter`
* `tt-streaming-get-firehose`

All tools have an `--output-file` argument. If omitted, the standard output pipe is used.

Additionally, all tools also have a `--resume` flag to indicate that you want to append data to an existing output file instead of truncating it. Beware that this option does not de-duplicate existing data.

Example usage:

    tt-streaming-get-sample --output-file tweets.json
    tt-streaming-get-filter --track obama trump --follow 6456345 --resume
    tt-streaming-get-filter --locations -122.75 36.8 -121.75 37.8 -74 40 -73 41
    tt-streaming-get-firehose

## Tools for Tweets

* `tt-tweets-get-hydrated`
* `tt-tweets-get-retweets`
* `tt-tweets-get-timeline`
* `tt-tweets-search`

All tools have an `--output-file` argument. If omitted, the standard output is used.

Additionally, all tools also have a `--resume` flag to indicate that you want to append data to an existing output file instead of truncating it. Beware that this option does not de-duplicate existing data.

Example usage:

    tt-tweets-get-hydrated --tweet-ids tweet_ids.txt --output-file tweets.json
    tt-tweets-get-retweets --tweet-id 64563457564
    tt-tweets-get-timeline --screen-name insight_centre
    tt-tweets-search --query "twitter api" --resume

## Tools for Twitter Users

* `tt-users-get-hydrated`
* `tt-users-get-followers`
* `tt-users-get-friends`
* `tt-users-search`

All tools have an `--output-file` argument. If omitted, the standard output is used.

Additionally, all tools also have a `--resume` flag to indicate that you want to append data to an existing output file instead of truncating it. Beware that this option does not de-duplicate existing data.

Example usage:

    tt-users-get-hydrated --user-ids user_ids.txt --screen-names screen_names.txt
    tt-users-get-followers --user-id 54252345
    tt-users-get-friends --screen-name insight_centre --resume
    tt-users-search --query "rte" --output-file users.json

## Tools for Bulk Processing

* `tt-tweets-bulk-get-retweets`
* `tt-tweets-bulk-get-timeline`
* `tt-tweets-bulk-search`
* `tt-users-bulk-get-followers`
* `tt-users-bulk-get-friends`
* `tt-users-bulk-search`

All tools have an `--output-dir` argument. The directory is automatically created if not found. Some tools support resuming the bulk processing according to existing files in the output directory.

Example usage:

    tt-tweets-bulk-get-retweets --output-dir retweets --tweet-ids tweet_ids.txt
    tt-tweets-bulk-get-timeline --output-dir timelines --screen-names screen_names.txt
    tt-tweets-bulk-search --output-dir searches --queries queries.txt
    tt-users-bulk-get-followers --output-dir followers --user-ids user_ids.txt
    tt-users-bulk-get-friends --output-dir friends --screen_names screen_names.txt
    tt-users-bulk-search --output-dir searches --queries queries.txt

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

