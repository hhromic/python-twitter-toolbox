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

"""Twitter Public Streaming API module."""

import logging
import json
import time
from tweepy import StreamListener, Stream
from .helpers import init_logger, read_config, get_oauth_api
from .helpers import ensure_at_least_one

# module constants
RETRY_INTERVAL = 3

# module logging
LOGGER = logging.getLogger(__name__)
init_logger(LOGGER)

class PassThroughStreamListener(StreamListener):
    """Stream Listener that passes incoming messages directly to a writer."""

    def __init__(self, writer, limit=0, **kwargs):
        super(PassThroughStreamListener, self).__init__(**kwargs)
        self.writer = writer
        self.limit = limit
        self.num_written = 0

    def on_status(self, status):
        """Write an incoming Tweet to the writer."""
        self.writer.write("%s\n" % json.dumps(status._json, separators=(",", ":")))  # pylint: disable=protected-access
        self.num_written += 1
        if self.num_written == self.limit:
            return False
        return True

    def on_error(self, status_code):
        """Handle stream errors."""
        if status_code == 420:
            LOGGER.error("too many connection attempts, stopping stream")
            return False
        return True

def _get_stream(writer, config, limit=0):
    api = get_oauth_api(config)
    listener = PassThroughStreamListener(writer, limit=limit)
    return Stream(auth=api.auth, listener=listener)

def _safe_stream_run(func, *args, **kwargs):
    running = True
    while running:
        try:
            func(*args, **kwargs)
            running = False
        except Exception as excp:  # pylint: disable=broad-except
            LOGGER.warning(excp)
            LOGGER.info("reconnecting stream ...")
            time.sleep(RETRY_INTERVAL)

def get_sample(writer):
    """Get hydrated Tweet-objects from the sample Streaming API endpoint."""
    LOGGER.info("get_sample() starting")

    # initialize a Streaming API object and run the endpoint
    config = read_config()
    limit = config.getint("sample", "limit")
    stream = _get_stream(writer, config, limit=limit)
    _safe_stream_run(stream.sample)

    # finished
    LOGGER.info("get_sample() finished")

def get_filter(writer, follow=None, track=None, locations=None):
    """Get hydrated Tweet-objects from the filter Streaming API endpoint."""
    LOGGER.info("get_filter() starting")
    ensure_at_least_one(follow=follow, track=track, locations=locations)
    follow = [str(f) for f in follow] if follow else None

    # initialize a Streaming API object and run the endpoint
    config = read_config()
    limit = config.getint("filter", "limit")
    stream = _get_stream(writer, config, limit=limit)
    _safe_stream_run(stream.filter, follow=follow, track=track, locations=locations)

    # finished
    LOGGER.info("get_filter() finished")

def get_firehose(writer):
    """Get hydrated Tweet-objects from the firehose Streaming API endpoint."""
    LOGGER.info("get_firehose() starting")

    # initialize a Streaming API object and run the endpoint
    config = read_config()
    limit = config.getint("firehose", "limit")
    stream = _get_stream(writer, config, limit=limit)
    _safe_stream_run(stream.firehose)

    # finished
    LOGGER.info("get_firehose() finished")
