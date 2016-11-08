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

"""Google Compute Engine credentials.

This module provides authentication for application running on Google Compute
Engine using the Compute Engine metadata server.

"""

from google.auth import credentials
from google.auth import exceptions
from google.auth.compute_engine import _metadata


class Credentials(credentials.Scoped, credentials.Credentials):
    """Compute Engine Credentials.

    These credentials use the Google Compute Engine metadata server to obtain
    OAuth 2.0 access tokens associated with the instance's service account.

    For more information about Compute Engine authentication, including how
    to configure scopes, see the `Compute Engine authentication
    documentation`_.

    .. note:: Compute Engine instances can be created with scopes and therefore
        these credentials are considered to be 'scoped'. However, you can
        not use :meth:`~google.auth.credentials.ScopedCredentials.with_scopes`
        because it is not possible to change the scopes that the instance
        has. Also note that
        :meth:`~google.auth.credentials.ScopedCredentials.has_scopes` will not
        work until the credentials have been refreshed.

    .. _Compute Engine authentication documentation:
        https://cloud.google.com/compute/docs/authentication#using
    """

    def __init__(self, service_account_email='default'):
        """
        Args:
            service_account_email (str): The service account email to use, or
                'default'. A Compute Engine instance may have multiple service
                accounts.
        """
        super(Credentials, self).__init__()
        self._service_account_email = service_account_email

    def _retrieve_info(self, request):
        """Retrieve information about the service account.

        Updates the scopes and retrieves the full service account email.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.
        """
        info = _metadata.get_service_account_info(
            request,
            service_account=self._service_account_email)

        self._service_account_email = info['email']
        self._scopes = info['scopes']

    def refresh(self, request):
        """Refresh the access token and scopes.

        Args:
            request (google.auth.transport.Request): The object used to make
                HTTP requests.

        Raises:
            google.auth.exceptions.RefreshError: If the Compute Engine metadata
                service can't be reached if if the instance has not
                credentials.
        """
        try:
            self._retrieve_info(request)
            self.token, self.expiry = _metadata.get_service_account_token(
                request,
                service_account=self._service_account_email)
        except exceptions.TransportError as exc:
            raise exceptions.RefreshError(exc)

    @property
    def service_account_email(self):
        """The service account email.

        .. note: This is not guaranteed to be set until :meth`refresh` has been
            called.
        """
        return self._service_account_email

    @property
    def requires_scopes(self):
        """False: Compute Engine credentials can not be scoped."""
        return False

    def with_scopes(self, scopes):
        """Unavailable, Compute Engine credentials can not be scoped.

        Scopes can only be set at Compute Engine instance creation time.
        See the `Compute Engine authentication documentation`_ for details on
        how to configure instance scopes.

        .. _Compute Engine authentication documentation:
            https://cloud.google.com/compute/docs/authentication#using
        """
        raise NotImplementedError(
            'Compute Engine credentials can not set scopes. Scopes must be '
            'set when the Compute Engine instance is created.')
