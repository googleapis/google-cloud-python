# Copyright 2015 Google Inc. All rights reserved.
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

"""Helper functions for shared behavior."""


def _format_timestamp(timestamp):
    """Convert a datetime object to a string as required by the API.

    :type timestamp: :class:`datetime.datetime`
    :param timestamp: A datetime object.

    :rtype: string
    :returns: The formatted timestamp. For example:
        ``"2016-02-17T19:18:01.763000Z"``
    """
    if timestamp.tzinfo is not None:
        # Convert to UTC and remove the time zone info.
        timestamp = timestamp.replace(tzinfo=None) - timestamp.utcoffset()

    return timestamp.isoformat() + 'Z'
