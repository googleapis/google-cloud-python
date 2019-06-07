# Copyright 2019 Google LLC
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

"""Client options class.

Client options provide an consistent interface for user options to be defined
across clients.
"""


class ClientOptions(object):
    """Client Options used to set options on clients.

    Args:
        options (dict): A dict of the options listed below.
        api_endpoint (str): The desired API endpoint, e.g., compute.googleapis.com
    """

    api_endpoint = None

    def __init__(self, options=None, **kw_args):
        if options is not None:
            if kw_args.items():
                raise Exception(
                    "ClientOptions expects options in a dictionary or in kw_args, not both"
                )
            client_options = options
        else:
            client_options = kw_args

        for key, value in client_options.items():
            if not hasattr(self, key):
                raise ValueError(
                    "ClientOptions does not accept an argument named '" + key + "'"
                )
            setattr(self, key, value)
