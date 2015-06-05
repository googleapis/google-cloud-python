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

"""gcloud pubsub client for interacting with API."""


from gcloud._helpers import _get_production_project
from gcloud.credentials import get_credentials
from gcloud.pubsub.connection import Connection


class Client(object):
    """Client to bundle configuration needed for API requests.

    :type project: string
    :param project: the project which the client acts on behalf of. Will be
                    passed when creating a topic.  If not passed,
                    falls back to the default inferred from the environment.

    :type credentials: :class:`oauth2client.client.OAuth2Credentials` or
                       :class:`NoneType`
    :param credentials: The OAuth2 Credentials to use for the connection
                        owned by this client. If not passed (and if no ``http``
                        object is passed), falls back to the default inferred
                        from the environment.

    :type http: :class:`httplib2.Http` or class that defines ``request()``.
    :param http: An optional HTTP object to make requests.

    :raises: :class:`ValueError` if the project is neither passed in nor
             set in the environment.
    """
    def __init__(self, project=None, credentials=None, http=None):
        if project is None:
            project = _get_production_project()
        if project is None:
            raise ValueError('Project was not passed and could not be '
                             'determined from the environment.')
        self.project = project

        if credentials is None and http is None:
            credentials = get_credentials()
        self.connection = Connection(credentials=credentials, http=http)
