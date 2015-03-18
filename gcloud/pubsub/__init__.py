"""Shortcut methods for getting set up with Google Cloud Pub/Sub.

You'll typically use these to get started with the API:

>>> from gcloud import pubsub
>>> connection = pubsub.get_connection('long-email@googleapis.com',
...                                    '/path/to/private.key')
>>> # Then do other things...
>>> topic = connection.create_topic('topic-name-here')
>>> topic.publish_message('My message', labels=['label1', 1234, 'label2']

The main concepts with this API are:

- :class:`gcloud.pubsub.connection.Connection`
  which represents a connection between your machine and Cloud Pub/Sub.

- :class:`gcloud.pubsub.topic.Topic`
  which represents a particular topic.

- :class:`gcloud.pubsub.subscription.Subscription`
  which represents a subscription to a topic.

- :class:`gcloud.pubsub.message.Message`
  which represents a message pulled from a Subscription.
"""

__version__ = '0.0.1'

SCOPE = ('https://www.googleapis.com/auth/pubsub',
         'https://www.googleapis.com/auth/cloud-platform')
"""The scope required for authenticating as a Cloud Pub/Sub consumer."""


def get_connection(client_email, private_key_path):
    """Shortcut method to establish a connection to Cloud Pub/Sub.

    Use this to quickly establish a connection to the Pub/Sub API.

    >>> from gcloud import pubsub
    >>> connection = pubsub.get_connection(email, key_path)
    >>> topic = connection.get_topic('topic-name')

    :type client_email: string
    :param client_email: The e-mail attached to the service account.

    :type private_key_path: string
    :param private_key_path: The path to a private key file (this file was
                             given to you when you created the service
                             account).

    :rtype: :class:`gcloud.pubsub.connection.Connection`
    :returns: A connection defined with the proper credentials.
    """
    from gcloud.credentials import Credentials
    from gcloud.pubsub.connection import Connection

    credentials = Credentials.get_for_service_account(
        client_email, private_key_path, scope=SCOPE)
    return Connection(credentials=credentials)
