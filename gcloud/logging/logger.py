# Copyright 2016 Google Inc. All rights reserved.
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

"""Define API Loggers."""


class Logger(object):
    """Loggers represent named targets for log entries.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.logs

    :type name: string
    :param name: the name of the logger

    :type client: :class:`gcloud.logging.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the logger (which requires a project).
    """
    def __init__(self, name, client):
        self.name = name
        self._client = client

    @property
    def client(self):
        """Clent bound to the logger."""
        return self._client

    @property
    def project(self):
        """Project bound to the logger."""
        return self._client.project
