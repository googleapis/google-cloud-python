"""A simple wrapper around the OAuth2 credentials library."""

from oauth2client import client


class Credentials(object):
  """An object used to simplify the OAuth2 credentials library.

  .. note::
    You should not need to use this class directly.
    Instead, use the helper methods provided in
    :func:`gcloud.datastore.__init__.get_connection`
    and
    :func:`gcloud.datastore.__init__.get_dataset`
    which use this class under the hood.
  """

  @classmethod
  def get_for_service_account(cls, client_email, private_key_path, scope=None):
    """Gets the credentials for a service account.

    :type client_email: string
    :param client_email: The e-mail attached to the service account.

    :type private_key_path: string
    :param private_key_path: The path to a private key file (this file was
                             given to you when you created the service
                             account).

    :type scope: string or tuple of strings
    :param scope: The scope against which to authenticate.
                  (Different services require different scopes,
                  check the documentation for which scope is required
                  for the different levels of access
                  to any particular API.)
    """
    return client.SignedJwtAssertionCredentials(
        service_account_name=client_email,
        private_key=open(private_key_path).read(),
        scope=scope)
