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

"""Useful constants need for Google Media Downloads and Resumable Uploads."""


UPLOAD_CHUNK_SIZE = 262144  # 256 * 1024
"""int: Chunks in a resumable upload must come in multiples of 256 KB."""
PERMANENT_REDIRECT = 308
"""int: Permanent redirect status code.

It is used by Google services to indicate some (but not all) of
a resumable upload has been completed.

``http.client.PERMANENT_REDIRECT`` was added in Python 3.5, so
can't be used in a "general" code base.

For more information, see `RFC 7238`_.

.. _RFC 7238: https://tools.ietf.org/html/rfc7238
"""
TOO_MANY_REQUESTS = 429
"""int: Status code indicating rate-limiting.

``http.client.TOO_MANY_REQUESTS`` was added in Python 3.3, so
can't be used in a "general" code base.

For more information, see `RFC 6585`_.

.. _RFC 6585: https://tools.ietf.org/html/rfc6585#section-4
"""
