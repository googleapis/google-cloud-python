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

"""Custom exception types upload and downloads."""


class InvalidResponse(Exception):
    """Error class for responses which are not in the correct state.

    Args:
        response (object): The HTTP response which caused the failure.
        args (tuple): The positional arguments typically passed to an
            exception class.
    """

    def __init__(self, response, *args):
        super(InvalidResponse, self).__init__(*args)
        self.response = response
        """object: The HTTP response object that caused the failure."""
