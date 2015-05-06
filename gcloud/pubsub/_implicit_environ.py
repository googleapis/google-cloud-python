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

"""Module to provide implicit behavior based on enviroment.

Allows the pubsub package to infer the default connection from the enviroment.
"""


class _DefaultsContainer(object):
    """Container for defaults.

    :type connection: :class:`gcloud.pubsub.connection.Connection`
    :param connection: Persistent implied connection from environment.
    """

    def __init__(self, connection=None):
        self.connection = connection


def get_default_connection():
    """Get default connection.

    :rtype: :class:`gcloud.pubsub.connection.Connection` or ``NoneType``
    :returns: The default connection if one has been set.
    """
    return _DEFAULTS.connection


def _require_connection(connection=None):
    """Infer a connection from the environment, if not passed explicitly.

    :type connection: :class:`gcloud.pubsub.connection.Connection`
    :param connection: Optional.

    :rtype: :class:`gcloud.pubsub.connection.Connection`
    :returns: A connection based on the current environment.
    :raises: :class:`EnvironmentError` if ``connection`` is ``None``, and
             cannot be inferred from the environment.
    """
    if connection is None:
        connection = get_default_connection()

    if connection is None:
        raise EnvironmentError('Connection could not be inferred.')

    return connection


_DEFAULTS = _DefaultsContainer()
