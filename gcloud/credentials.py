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

import argparse
import json
import os
import sys
import tempfile
import six

from oauth2client import client
from oauth2client import file
from oauth2client import tools


def get_credentials():
    """Gets credentials implicitly from the current environment.

    .. note::
      You should not need to use this function directly. Instead, use the
      helper method :func:`gcloud.datastore.__init__.get_connection`
      which uses this method under the hood.

    Checks environment in order of precedence:
    - Google App Engine (production and testing)
    - Environment variable GOOGLE_APPLICATION_CREDENTIALS pointing to
      a file with stored credentials information.
    - Stored "well known" file associated with ``gcloud`` command line tool.
    - Google Compute Engine production environment.

    The file referred to in GOOGLE_APPLICATION_CREDENTIALS is expected to
    contain information about credentials that are ready to use. This means
    either service account information or user account information with
    a ready-to-use refresh token::

      {                                       {
          'type': 'authorized_user',              'type': 'service_account',
          'client_id': '...',                     'client_id': '...',
          'client_secret': '...',       OR        'client_email': '...',
          'refresh_token': '...,                  'private_key_id': '...',
      }                                           'private_key': '...',
                                              }

    The second of these is simply a JSON key downloaded from the Google APIs
    console. The first is a close cousin of the "client secrets" JSON file
    used by ``oauth2client.clientsecrets`` but differs in formatting.

    :rtype: :class:`oauth2client.client.GoogleCredentials`,
            :class:`oauth2client.appengine.AppAssertionCredentials`,
            :class:`oauth2client.gce.AppAssertionCredentials`,
            :class:`oauth2client.service_account._ServiceAccountCredentials`
    :returns: A new credentials instance corresponding to the implicit
              environment.
    """
    return client.GoogleCredentials.get_application_default()


def _store_user_credential(credential):
    """Stores a user credential as a well-known file.

    Prompts user first if they want to store the minted token and
    then prompts the user for a filename to store the token
    information in the format needed for get_credentials().

    :type credential: :class:`oauth2client.client.OAuth2Credentials`
    :param credential: A user credential to be stored.
    """
    ans = six.moves.input('Would you like to store your tokens '
                          'for future use? [y/n] ')
    if ans.strip().lower() != 'y':
        return

    filename = six.moves.input('Please name the file where you wish '
                               'to store them: ').strip()

    payload = {
        'client_id': credential.client_id,
        'client_secret': credential.client_secret,
        'refresh_token': credential.refresh_token,
        'type': 'authorized_user',
    }
    with open(filename, 'w') as file_obj:
        json.dump(payload, file_obj, indent=2, sort_keys=True,
                  separators=(',', ': '))
        file_obj.write('\n')

    print 'Saved %s' % (filename,)
    print 'If you would like to use these credentials in the future'
    print 'without having to initiate the authentication flow in your'
    print 'browser, please set the GOOGLE_APPLICATION_CREDENTIALS'
    print 'environment variable:'
    print '    export GOOGLE_APPLICATION_CREDENTIALS=%r' % (filename,)
    print 'Once you\'ve done this, you can use the get_credentials()'
    print 'function, which relies on that environment variable.'
    print ''
    print 'Keep in mind, the refresh token can only be used with the'
    print 'scopes you granted in the original authorization.'


def get_credentials_from_user_flow(scope, client_secrets_file=None):
    """Gets credentials by taking user through 3-legged auth flow.

    The necessary information to perform the flow will be stored in a client
    secrets file. This can be downloaded from the Google Cloud Console. First,
    visit "APIs & auth > Credentials", and creating a new client ID for an
    "Installed application" (or use an existing "Client ID for native
    application"). Then click "Download JSON" on your chosen "Client ID for
    native application" and save the client secrets file.

    You can either pass this filename in directly via 'client_secrets_file'
    or set the environment variable GCLOUD_CLIENT_SECRETS.

    For more information, see:
      developers.google.com/api-client-library/python/guide/aaa_client_secrets

    :type scope: string or tuple of string
    :param scope: The scope against which to authenticate. (Different services
                  require different scopes, check the documentation for which
                  scope is required for the different levels of access to any
                  particular API.)

    :type client_secrets_file: string
    :param client_secrets_file: Optional. File containing client secrets JSON.

    :rtype: :class:`oauth2client.client.OAuth2Credentials`
    :returns: A new credentials instance.
    :raises: ``EnvironmentError`` if stdout is not a TTY,
             ``ValueError`` if ``client_secrets_file`` is not passed in as an
             argument or set as an environment variable, or
             ``ValueError`` if the client secrets file is not for an installed
             application.
    """
    if not sys.stdout.isatty():
        raise EnvironmentError('Cannot initiate user flow unless user can '
                               'interact with standard out.')

    if client_secrets_file is None:
        client_secrets_file = os.getenv('GCLOUD_CLIENT_SECRETS')

    if client_secrets_file is None:
        raise ValueError('Client secrets file not specified.')

    client_type, client_info = client.clientsecrets.loadfile(
        client_secrets_file)
    if client_type != client.clientsecrets.TYPE_INSTALLED:
        raise ValueError('Client secrets file must be for '
                         'installed application.')

    redirect_uri = client_info['redirect_uris'][0]
    flow = client.flow_from_clientsecrets(client_secrets_file, scope,
                                          redirect_uri=redirect_uri)

    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args()
    storage = file.Storage(tempfile.mktemp())
    credential = tools.run_flow(flow, storage, flags)
    # Remove the tempfile as a store for the credentials to prevent
    # future writes to a non-existent file.
    credential.store = None
    # Determine if the user would like to store these credentials.
    _store_user_credential(credential)
    return credential


def get_for_service_account_p12(client_email, private_key_path, scope=None):
    """Gets the credentials for a service account.

    .. note::
      This method is not used by default, instead :func:`get_credentials`
      is used. This method is intended to be used when the environments is
      known explicitly and detecting the environment implicitly would be
      superfluous.

    :type client_email: string
    :param client_email: The e-mail attached to the service account.

    :type private_key_path: string
    :param private_key_path: The path to a private key file (this file was
                             given to you when you created the service
                             account). This file must be in P12 format.

    :type scope: string or tuple of string
    :param scope: The scope against which to authenticate. (Different services
                  require different scopes, check the documentation for which
                  scope is required for the different levels of access to any
                  particular API.)

    :rtype: :class:`oauth2client.client.SignedJwtAssertionCredentials`
    :returns: A new ``SignedJwtAssertionCredentials`` instance with the
              needed service account settings.
    """
    return client.SignedJwtAssertionCredentials(
        service_account_name=client_email,
        private_key=open(private_key_path, 'rb').read(),
        scope=scope)
