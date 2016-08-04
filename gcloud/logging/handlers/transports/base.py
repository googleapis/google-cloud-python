# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Base class for Python logging handler Transport objects"""


class Transport(object):
    """Base class for gcloud logging handler Transports.
    Subclasses of Transports must have constructors that accept a client and
    name object, and must override the send method.
    """

    def __init__(self, client, name):
        pass  # pragma: NO COVER

    def send(self, kwargs):
        """Must be overriden by transport options. kwargs is the dictionary
        with keyword arguments which will be passed to
        :method:`gcloud.logging.Logger.log_struct()`.

        :type kwargs: dict
        :param kwargs: {'info': ..., 'severity': ...} - keyword arguments
                       passed to :method:`gcloud.logging.Logger.log_struct()`.
        """
        raise NotImplementedError()
