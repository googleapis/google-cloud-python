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

"""A Client for interacting with the Resource Manager API."""


from gcloud.client import Client as BaseClient
from gcloud.resource_manager.connection import Connection
from gcloud.resource_manager.project import Project


class Client(BaseClient):
    """Client to bundle configuration needed for API requests.

    See
    https://cloud.google.com/resource-manager/reference/rest/
    for more information on this API.

    Automatically get credentials::

        >>> from gcloud import resource_manager
        >>> client = resource_manager.Client()

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.
    """

    _connection_class = Connection

    def project(self, project_id, name=None, labels=None):
        """Creates a :class:`.Project` bound to the current client.

        .. note:

            This does not make an API call.

        :type project_id: str
        :param project_id: The ID for this project.

        :type name: string
        :param name: The display name of the project.

        :type labels: dict
        :param labels: A list of labels associated with the project.

        :rtype: :class:`.Project`
        :returns: A new instance of a :class:`.Project` **without**
                  any metadata loaded.
        """
        return Project(project_id=project_id,
                       client=self, name=name, labels=labels)
