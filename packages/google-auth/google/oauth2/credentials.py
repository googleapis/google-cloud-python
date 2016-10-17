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

"""OAuth 2.0 Credentials.

This module provides credentials based on OAuth 2.0 access and refresh tokens.
These credentials usually access resources on behalf of a user (resource
owner).

Specifically, this is intended to use access tokens acquired using the
`Authorization Code grant`_ and can refresh those tokens using a
optional `refresh token`_.

Obtaining the initial access and refresh token is outside of the scope of this
module. Consult `rfc6749 section 4.1`_ for complete details on the
Authorization Code grant flow.

.. _Authorization Code grant: https://tools.ietf.org/html/rfc6749#section-1.3.1
.. _refresh token: https://tools.ietf.org/html/rfc6749#section-6
.. _rfc6749 section 4.1: https://tools.ietf.org/html/rfc6749#section-4.1
"""

from google.auth import _helpers
from google.auth import credentials
from google.oauth2 import _client


class Credentials(credentials.Scoped, credentials.Credentials):
    """Credentials using OAuth 2.0 access and refresh tokens."""

    def __init__(self, token, refresh_token=None, token_uri=None,
                 client_id=None, client_secret=None, scopes=None):
        """
        Args:
            token (Optional(str)): The OAuth 2.0 access token. Can be None
                if refresh information is provided.
            refresh_token (str): The OAuth 2.0 refresh token. If specified,
                credentials can be refreshed.
            token_uri (str): The OAuth 2.0 authorization server's token
                endpoint URI. Must be specified for refresh, can be left as
                None if the token can not be refreshed.
            client_id (str): The OAuth 2.0 client ID. Must be specified for
                refresh, can be left as None if the token can not be refreshed.
            client_secret(str): The OAuth 2.0 client secret. Must be specified
                for refresh, can be left as None if the token can not be
                refreshed.
            scopes (Sequence[str]): The scopes that were originally used
                to obtain authorization. This is a purely informative parameter
                that can be used by :meth:`has_scopes`. OAuth 2.0 credentials
                can not request additional scopes after authorization.
        """
        super(Credentials, self).__init__()
        self.token = token
        self._refresh_token = refresh_token
        self._scopes = scopes
        self._token_uri = token_uri
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def requires_scopes(self):
        """False: OAuth 2.0 credentials have their scopes set when
        the initial token is requested and can not be changed."""
        return False

    def with_scopes(self, scopes):
        """Unavailable, OAuth 2.0 credentials can not be re-scoped.

        OAuth 2.0 credentials have their scopes set when the initial token is
        requested and can not be changed.
        """
        raise NotImplementedError(
            'OAuth 2.0 Credentials can not modify their scopes.')

    @_helpers.copy_docstring(credentials.Credentials)
    def refresh(self, request):
        access_token, refresh_token, expiry, _ = _client.refresh_grant(
            request, self._token_uri, self._refresh_token, self._client_id,
            self._client_secret)

        self.token = access_token
        self.expiry = expiry
        self._refresh_token = refresh_token
