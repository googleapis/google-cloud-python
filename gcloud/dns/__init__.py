"""Shortcut methods for getting set up with Google Cloud DNS.

You'll typically use these to get started with the API:

>>> import gcloud.dns
>>> zone = gcloud.dns.get_zone('zone-name-here',
                                     'long-email@googleapis.com',
                                     '/path/to/private.key')

The main concepts with this API are:

- :class:`gcloud.dns.connection.Connection`
  which represents a connection between your machine
  and the Cloud DNS API.

- :class:`gcloud.dns.zone.Zone`
  which represents a particular zone.
"""


__version__ = '0.1'

# TODO: Allow specific scopes and authorization levels.
SCOPE = ('https://www.googleapis.com/auth/cloud-platform',
         'https://www.googleapis.com/auth/ndev.clouddns.readonly',
         'https://www.googleapis.com/auth/ndev.clouddns.readwrite')
"""The scope required for authenticating as a Cloud DNS consumer."""


def get_connection(project, client_email, private_key_path):
  """Shortcut method to establish a connection to Cloud DNS.

  Use this if you are going to access several zones
  with the same set of credentials:

  >>> from gcloud import dns
  >>> connection = dns.get_connection(project, email, key_path)
  >>> zone1 = connection.get_zone('zone1')
  >>> zone2 = connection.get_zone('zone2')

  :type project: string
  :param project: The name of the project to connect to.

  :type client_email: string
  :param client_email: The e-mail attached to the service account.

  :type private_key_path: string
  :param private_key_path: The path to a private key file (this file was
                           given to you when you created the service
                           account).

  :rtype: :class:`gcloud.dns.connection.Connection`
  :returns: A connection defined with the proper credentials.
  """

  from gcloud.credentials import Credentials
  from gcloud.dns.connection import Connection

  credentials = Credentials.get_for_service_account(
      client_email, private_key_path, scope=SCOPE)
  return Connection(project=project, credentials=credentials)


def get_zone(zone, project, client_email, private_key_path):
  """Shortcut method to establish a connection to a particular zone.

  You'll generally use this as the first call to working with the API:

  >>> from gcloud import dns
  >>> zone = dns.get_zone(zone, project, email, key_path)

  :type zone: string
  :param zone: The id of the zone you want to use.
                    This is akin to a disk name on a file system.

  :type project: string
  :param project: The name of the project to connect to.

  :type client_email: string
  :param client_email: The e-mail attached to the service account.

  :type private_key_path: string
  :param private_key_path: The path to a private key file (this file was
                           given to you when you created the service
                           account).

  :rtype: :class:`gcloud.dns.zone.Zone`
  :returns: A zone with a connection using the provided credentials.
  """

  connection = get_connection(project, client_email, private_key_path)
  return connection.get_zone(zone)
