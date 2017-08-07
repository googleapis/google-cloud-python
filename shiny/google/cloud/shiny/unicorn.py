# Copyright 2016 Google Inc.
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

"""Defines Google Shiny New API :class:`Unicorn` class."""


class Unicorn(object):
    """A representation of the Shiny API's favorite noun: Unicorn.

    :type name: str
    :param name: The name of the unicorn.

    :type client: :class:`~google.cloud.shiny.client.Client`
    :param client: The client that owns the current unicorn.
    """

    def __init__(self, name, client):
        self._name = name
        self._client = client

    @property
    def name(self):
        """The name of the current unicorn.

        .. note::

            This is a read-only property.

        :rtype: str
        :returns: The name of the current unicorn.
        """
        return self._name

    @property
    def client(self):
        """The client that owns the current unicorn.

        .. note::

            This is a read-only property.

        :rtype: :class:`~google.cloud.shiny.client.Client`
        :returns: The client that owns the current unicorn.
        """
        return self._client

    def do_nothing(self):
        """Send the current unicorn to Shiny API's "do nothing" method."""
        self._client.shiny_api.do_nothing(self.name)
