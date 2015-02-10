# Copyright 2014 Google Inc. All rights reserved.
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

"""GCloud API access in idiomatic Python."""

from pkg_resources import get_distribution

import six
import socket

try:
    from google import appengine
except ImportError:
    appengine = None


__version__ = get_distribution('gcloud').version


HTTPConnection = six.moves.http_client.HTTPConnection


class _UserAgentReifyProperty(object):
    """Helper for extra environment information."""

    _curr_environ = None
    _user_agent = None

    def __init__(self, wrapped):
        self._property_name = wrapped.__name__
        self._curr_environ = self.environ_at_init()

    @staticmethod
    def environ_at_init():
        """Checks environment variables during instance initialization.

        Intended to infer as much as possible from the environment without
        running code.

        :rtype: string or ``NoneType``
        :returns: Either ``'-GAE'`` if on App Engine else ``None``
        """
        if appengine is not None:
            return '-GAE'

    def environ_post_init(self):
        """Checks environment variables after instance initialization.

        This is meant for checks which can't be performed instantaneously.

        :rtype: string
        :returns: Either ``'-GCE'`` if on Compute Engine else an empty string.
        """
        gce_environ = self.check_compute_engine()
        if gce_environ is not None:
            return gce_environ

        return ''

    @staticmethod
    def check_compute_engine():
        """Checks if the current environment is Compute Engine.

        :rtype: string or ``NoneType``
        :returns: The string ``'-GCE'`` if on Compute Engine else ``None``.
        """
        host = '169.254.169.254'
        uri_path = '/computeMetadata/v1/project/project-id'
        headers = {'Metadata-Flavor': 'Google'}
        connection = HTTPConnection(host, timeout=0.1)
        try:
            connection.request('GET', uri_path, headers=headers)
            response = connection.getresponse()
            if response.status == 200:
                return '-GCE'
        except socket.error:  # Expect timeout or host is down
            pass
        finally:
            connection.close()

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self

        if self._curr_environ is None:
            self._curr_environ = self.environ_post_init()

        if self._user_agent is None:
            self._user_agent = "gcloud-python/{0}{1}".format(
                __version__, self._curr_environ)

        setattr(inst, self._property_name, self._user_agent)
        return self._user_agent
