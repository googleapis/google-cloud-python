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


from gooresmed import exceptions


def header_required(response, name):
    """Checks that a specific header is in a headers dictionary.

    Args:
        response (object): An HTTP response object, expected to have a
            ``headers`` attribute that is a ``Mapping[str, str]``.
        name (str): The name of a required header.

    Returns:
        str: The desired header.

    Raises:
        ~gooresmed.exceptions.InvalidResponse: If the header is missing.
    """
    headers = response.headers
    if name not in headers:
        raise exceptions.InvalidResponse(
            response, u'Response headers must contain header', name)

    return headers[name]


def get_status_code(response):
    """Access the status code from an HTTP response.

    Args:
        response (object): The HTTP response object.

    Returns:
        int: The status code.
    """
    return response.status_code
