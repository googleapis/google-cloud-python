# Copyright 2015 Google Inc.
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

"""Base classes for client used to interact with Google Cloud APIs."""

import google.auth.credentials
from google.oauth2 import service_account
import six

from google.cloud._helpers import _determine_default_project
from google.cloud._http import Connection
from google.cloud.credentials import get_credentials


_GOOGLE_AUTH_CREDENTIALS_HELP = (
    'This library only supports credentials from google-auth-library-python. '
    'See https://google-cloud-python.readthedocs.io/en/latest/'
    'google-cloud-auth.html for help on authentication with this library.'
)


class _ClientFactoryMixin(object):
    """Mixin to allow factories that create credentials.

    .. note::

        This class is virtual.
    """

    @classmethod
    def from_service_account_json(cls, json_credentials_path, *args, **kwargs):
        """Factory to retrieve JSON credentials while creating client.

        :type json_credentials_path: str
        :param json_credentials_path: The path to a private key file (this file
                                      was given to you when you created the
                                      service account). This file must contain
                                      a JSON object with a private key and
                                      other credentials information (downloaded
                                      from the Google APIs console).

        :type args: tuple
        :param args: Remaining positional arguments to pass to constructor.

        :type kwargs: dict
        :param kwargs: Remaining keyword arguments to pass to constructor.

        :rtype: :class:`google.cloud.pubsub.client.Client`
        :returns: The client created with the retrieved JSON credentials.
        :raises: :class:`TypeError` if there is a conflict with the kwargs
                 and the credentials created by the factory.
        """
        if 'credentials' in kwargs:
            raise TypeError('credentials must not be in keyword arguments')
        credentials = service_account.Credentials.from_service_account_file(
            json_credentials_path)
        kwargs['credentials'] = credentials
        return cls(*args, **kwargs)


class Client(_ClientFactoryMixin):
    """Client to bundle configuration needed for API requests.

    Assumes that the associated ``_connection_class`` only accepts
    ``http`` and ``credentials`` in its constructor.

    :type credentials: :class:`google.auth.credentials.Credentials` or
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

    def __init__(self, credentials=None, http=None):
        if (credentials is not None and
                not isinstance(
                    credentials, google.auth.credentials.Credentials)):
            raise ValueError(_GOOGLE_AUTH_CREDENTIALS_HELP)
        if credentials is None and http is None:
            credentials = get_credentials()
        self._connection = self._connection_class(
            credentials=credentials, http=http)


class _ClientProjectMixin(object):
    """Mixin to allow setting the project on the client.

    :type project: str
    :param project: the project which the client acts on behalf of. If not
                    passed falls back to the default inferred from the
                    environment.

    :raises: :class:`EnvironmentError` if the project is neither passed in nor
             set in the environment. :class:`ValueError` if the project value
             is invalid.
    """

    def __init__(self, project=None):
        project = self._determine_default(project)
        if project is None:
            raise EnvironmentError('Project was not passed and could not be '
                                   'determined from the environment.')
        if isinstance(project, six.binary_type):
            project = project.decode('utf-8')
        if not isinstance(project, six.string_types):
            raise ValueError('Project must be a string.')
        self.project = project

    @staticmethod
    def _determine_default(project):
        """Helper:  use default project detection."""
        return _determine_default_project(project)


class JSONClient(Client, _ClientProjectMixin):
    """Client for Google JSON-based API.

    Assumes such APIs use the ``project`` and the client needs to store this
    value.

    :type project: str
    :param project: the project which the client acts on behalf of. If not
                    passed falls back to the default inferred from the
                    environment.

    :type credentials: :class:`google.auth.credentials.Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests. If not passed, an
                 ``http`` object is created that is bound to the
                 ``credentials`` for the current object.

    :raises: :class:`ValueError` if the project is neither passed in nor
             set in the environment.
    """

    def __init__(self, project=None, credentials=None, http=None):
        _ClientProjectMixin.__init__(self, project=project)
        Client.__init__(self, credentials=credentials, http=http)
