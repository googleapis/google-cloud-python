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

"""GCloud Pubsub API wrapper.


The main concepts with this API are:

- :class:`gcloud.pubsub.topic.Topic` represents an endpoint to which messages
  can be published using the Cloud Storage Pubsub API.

- :class:`gcloud.pubsub.subscription.Subscription` represents a named
  subscription (either pull or push) to a topic.
"""

from gcloud._helpers import get_default_project
from gcloud._helpers import set_default_project
from gcloud.connection import get_scoped_connection
from gcloud.pubsub import _implicit_environ
from gcloud.pubsub._implicit_environ import get_default_connection
from gcloud.pubsub.api import list_topics
from gcloud.pubsub.connection import Connection


SCOPE = ('https://www.googleapis.com/auth/pubsub',
         'https://www.googleapis.com/auth/cloud-platform')


def set_default_connection(connection=None):
    """Set default connection either explicitly or implicitly as fall-back.

    :type connection: :class:`gcloud.pubsub.connection.Connection`
    :param connection: A connection provided to be the default.
    """
    _implicit_environ._DEFAULTS.connection = connection or get_connection()


def set_defaults(project=None, connection=None):
    """Set defaults either explicitly or implicitly as fall-back.

    Uses the arguments to call the individual default methods.

    :type project: string
    :param project: Optional. The name of the project to connect to.

    :type connection: :class:`gcloud.pubsub.connection.Connection`
    :param connection: Optional. A connection provided to be the default.
    """
    set_default_project(project=project)
    set_default_connection(connection=connection)


def get_connection():
    """Shortcut method to establish a connection to Cloud Storage.

    Use this if you are going to access several buckets with the same
    set of credentials:

    >>> from gcloud import pubsub
    >>> connection = pubsub.get_connection()
    >>> bucket1 = pubsub.get_bucket('bucket1', connection=connection)
    >>> bucket2 = pubsub.get_bucket('bucket2', connection=connection)

    :rtype: :class:`gcloud.pubsub.connection.Connection`
    :returns: A connection defined with the proper credentials.
    """
    return get_scoped_connection(Connection, SCOPE)
