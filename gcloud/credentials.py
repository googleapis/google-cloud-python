"""A simple wrapper around the OAuth2 credentials library."""

import base64
import calendar
import datetime
import urllib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from oauth2client import client
from OpenSSL import crypto
import pytz


def _utcnow():  # pragma: NO COVER testing replaces
    """Returns current time as UTC datetime.

    NOTE: on the module namespace so tests can replace it.
    """
    return datetime.datetime.utcnow()


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
        private_key=open(private_key_path).read(),
        scope=scope)


def generate_signed_url(credentials, endpoint, resource, expiration,
                        method='GET', content_md5=None, content_type=None):
    """Generate signed URL to provide query-string auth'n to a resource.

    :type credentials:
        :class:`oauth2client.client.SignedJwtAssertionCredentials`
    :param credentials: the credentials used to sign the URL.

    :type endpoint: string
    :param endpoint: Base API endpoint URL.

    :type resource: string
    :param resource: A pointer to a specific resource within the endpoint
                     (e.g., ``/bucket-name/file.txt``).

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :type method: string
    :param method: The HTTP verb that will be used when requesting the URL.

    :type content_md5: string
    :param content_md5: The MD5 hash of the object referenced by
                        ``resource``.

    :type content_type: string
    :param content_type: The content type of the object referenced by
                            ``resource``.

    :rtype: string
    :returns: A signed URL you can use to access the resource
                until expiration.
    """
    expiration = _get_expiration_seconds(expiration)

    # Generate the string to sign.
    signature_string = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        str(expiration),
        resource])

    # Take our PKCS12 (.p12) key and make it into a RSA key we can use...
    pkcs12 = crypto.load_pkcs12(
        base64.b64decode(credentials.private_key),
        'notasecret')
    pem = crypto.dump_privatekey(
        crypto.FILETYPE_PEM, pkcs12.get_privatekey())
    pem_key = RSA.importKey(pem)

    # Sign the string with the RSA key.
    signer = PKCS1_v1_5.new(pem_key)
    signature_hash = SHA256.new(signature_string)
    signature_bytes = signer.sign(signature_hash)
    signature = base64.b64encode(signature_bytes)

    # Set the right query parameters.
    query_params = {
        'GoogleAccessId': credentials.service_account_name,
        'Expires': str(expiration),
        'Signature': signature,
    }

    # Return the built URL.
    return '{endpoint}{resource}?{querystring}'.format(
        endpoint=endpoint, resource=resource,
        querystring=urllib.urlencode(query_params))


def _get_expiration_seconds(expiration):
    """Convert 'expiration' to a number of seconds in the future.

    :type expiration: int, long, datetime.datetime, datetime.timedelta
    :param expiration: When the signed URL should expire.

    :rtype: int
    :returns: a timestamp as an absolute number of seconds.
    """
    # If it's a timedelta, add it to `now` in UTC.
    if isinstance(expiration, datetime.timedelta):
        now = _utcnow().replace(tzinfo=pytz.utc)
        expiration = now + expiration

    # If it's a datetime, convert to a timestamp.
    if isinstance(expiration, datetime.datetime):
        # Make sure the timezone on the value is UTC
        # (either by converting or replacing the value).
        if expiration.tzinfo:
            expiration = expiration.astimezone(pytz.utc)
        else:
            expiration = expiration.replace(tzinfo=pytz.utc)

        # Turn the datetime into a timestamp (seconds, not microseconds).
        expiration = int(calendar.timegm(expiration.timetuple()))

    if not isinstance(expiration, (int, long)):
        raise TypeError('Expected an integer timestamp, datetime, or '
                        'timedelta. Got %s' % type(expiration))
    return expiration
