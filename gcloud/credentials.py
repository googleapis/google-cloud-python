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

"""A simple wrapper around the OAuth2 credentials library."""

from oauth2client import client


def get_for_service_account(client_email, private_key_path, scope=None):
    """Gets the credentials for a service account.

    .. note::
      You should not need to use this function directly.
      Instead, use the helper methods provided in
      :func:`gcloud.datastore.__init__.get_connection`
      and
      :func:`gcloud.datastore.__init__.get_dataset`
      which use this method under the hood.

    :type client_email: string
    :param client_email: The e-mail attached to the service account.

    :type private_key_path: string
    :param private_key_path: The path to a private key file (this file was
                             given to you when you created the service
                             account).

    :type scope: string or tuple of strings
    :param scope: The scope against which to authenticate. (Different services
                  require different scopes, check the documentation for which
                  scope is required for the different levels of access to any
                  particular API.)

    :rtype: :class:`oauth2client.client.SignedJwtAssertionCredentials`
    :returns: A new SignedJwtAssertionCredentials instance with the
              needed service account settings.
    """
    return client.SignedJwtAssertionCredentials(
        service_account_name=client_email,
        private_key=open(private_key_path, 'rb').read(),
        scope=scope)
