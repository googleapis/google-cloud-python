# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This program obtains a set of user credentials.

These credentials are needed to run the system test for OAuth2 credentials.
It's expected that a developer will run this program manually once to obtain
a refresh token. It's highly recommended to use a Google account created
specifically for testing.
"""

import json
import os

from oauth2client import client
from oauth2client import tools

HERE = os.path.dirname(__file__)
CLIENT_SECRETS_PATH = os.path.abspath(os.path.join(
    HERE, '..', 'system_tests', 'data', 'client_secret.json'))
AUTHORIZED_USER_PATH = os.path.abspath(os.path.join(
    HERE, '..', 'system_tests', 'data', 'authorized_user.json'))
SCOPES = ['email', 'profile']


class NullStorage(client.Storage):
    """Null storage implementation to prevent oauth2client from failing
    on storage.put."""
    def locked_put(self, credentials):
        pass


def main():
    flow = client.flow_from_clientsecrets(CLIENT_SECRETS_PATH, SCOPES)

    print('Starting credentials flow...')
    credentials = tools.run_flow(flow, NullStorage())

    # Save the credentials in the same format as the Cloud SDK's authorized
    # user file.
    data = {
        'type': 'authorized_user',
        'client_id': flow.client_id,
        'client_secret': flow.client_secret,
        'refresh_token': credentials.refresh_token
    }

    with open(AUTHORIZED_USER_PATH, 'w') as fh:
        json.dump(data, fh, indent=4)

    print('Created {}.'.format(AUTHORIZED_USER_PATH))

if __name__ == '__main__':
    main()
