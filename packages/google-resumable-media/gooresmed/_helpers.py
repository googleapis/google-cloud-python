# Copyright 2017 Google Inc.
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

"""Shared utilities used by both downloads and uploads."""


def header_required(headers, name):
    """Checks that a specific header is in a headers dictionary.

    Args:
        headers (Mapping[str, str]): The response headers from an HTTP request.
        name (str): The name of a required header.

    Returns:
        str: The desired header.

    Raises:
        KeyError: If the header is missing.
    """
    if name not in headers:
        msg = u'Response headers must contain {} header'.format(name)
        raise KeyError(msg)

    return headers[name]


def get_status_code(response):
    """Access the status code from an HTTP response.

    Args:
        response (object): The HTTP response object.

    Returns:
        int: The status code.
    """
    return response.status_code
