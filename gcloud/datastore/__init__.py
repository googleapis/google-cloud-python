"""Shortcut methods for getting set up with Google Cloud Datastore.

You'll typically use these to get started with the API:

>>> import gcloud.datastore
>>> dataset = gcloud.datastore.get_dataset('dataset-id-here',
                                          'long-email@googleapis.com',
                                          '/path/to/private.key')
>>> # Then do other things...
>>> query = dataset.query().kind('EntityKind')
>>> entity = dataset.entity('EntityKind')

The main concepts with this API are:

- :class:`gcloud.datastore.connection.Connection`
  which represents a connection between your machine and the Cloud Datastore
  API.

- :class:`gcloud.datastore.dataset.Dataset`
  which represents a particular dataset
  (akin to a database name in relational database world).

- :class:`gcloud.datastore.entity.Entity`
  which represents a single entity in the datastore
  (akin to a row in relational database world).

- :class:`gcloud.datastore.key.Key`
  which represents a pointer to a particular entity in the datastore
  (akin to a unique identifier in relational database world).

- :class:`gcloud.datastore.query.Query`
  which represents a lookup or search over the rows in the datastore.
"""


__version__ = '0.1.2'

SCOPE = ('https://www.googleapis.com/auth/datastore ',
         'https://www.googleapis.com/auth/userinfo.email')
"""The scope required for authenticating as a Cloud Datastore consumer."""


def get_connection(client_email, private_key_path):
  """Shortcut method to establish a connection to the Cloud Datastore.

  Use this if you are going to access several datasets
  with the same set of credentials (unlikely):

  >>> import gcloud.datastore
  >>> connection = gcloud.datastore.get_connection(email, key_path)
  >>> dataset1 = connection.dataset('dataset1')
  >>> dataset2 = connection.dataset('dataset2')

  :type client_email: string
  :param client_email: The e-mail attached to the service account.

  :type private_key_path: string
  :param private_key_path: The path to a private key file (this file was
                           given to you when you created the service
                           account).

  :rtype: :class:`gcloud.datastore.connection.Connection`
  :returns: A connection defined with the proper credentials.
  """
  from gcloud.credentials import Credentials
  from gcloud.datastore.connection import Connection

  credentials = Credentials.get_for_service_account(
      client_email, private_key_path, scope=SCOPE)
  return Connection(credentials=credentials)

def get_dataset(dataset_id, client_email, private_key_path):
  """Shortcut method to establish a connection to a particular dataset in the Cloud Datastore.

  You'll generally use this as the first call to working with the API:

  >>> import gcloud.datastore
  >>> dataset = gcloud.datastore.get_dataset('dataset-id', email, key_path)
  >>> # Now you can do things with the dataset.
  >>> dataset.query().kind('TestKind').fetch()
  [...]

  :type dataset_id: string
  :param dataset_id: The id of the dataset you want to use.
                     This is akin to a database name
                     and is usually the same as your Cloud Datastore project
                     name.

  :type client_email: string
  :param client_email: The e-mail attached to the service account.

  :type private_key_path: string
  :param private_key_path: The path to a private key file (this file was
                           given to you when you created the service
                           account).

  :rtype: :class:`gcloud.datastore.dataset.Dataset`
  :returns: A dataset with a connection using the provided credentials.
  """
  connection = get_connection(client_email, private_key_path)
  return connection.dataset(dataset_id)
