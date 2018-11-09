User Guide
==========

.. currentmodule:: google.auth

Credentials and account types
-----------------------------

:class:`~credentials.Credentials` are the means of identifying an application or
user to a service or API. Credentials can be obtained with two different types
of accounts: *service accounts* and *user accounts*.

Credentials from service accounts identify a particular application. These types
of credentials are used in server-to-server use cases, such as accessing a
database. This library primarily focuses on service account credentials.

Credentials from user accounts are obtained by asking the user to authorize
access to their data. These types of credentials are used in cases where your
application needs access to a user's data in another service, such as accessing
a user's documents in Google Drive. This library provides no support for
obtaining user credentials, but does provide limited support for using user
credentials.

Obtaining credentials
---------------------

.. _application-default:

Application default credentials
+++++++++++++++++++++++++++++++

`Google Application Default Credentials`_ abstracts authentication across the
different Google Cloud Platform hosting environments. When running on any Google
Cloud hosting environment or when running locally with the `Google Cloud SDK`_
installed, :func:`default` can automatically determine the credentials from the
environment::

    import google.auth

    credentials, project = google.auth.default()

If your application requires specific scopes::

    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

.. _Google Application Default Credentials:
    https://developers.google.com/identity/protocols/
    application-default-credentials
.. _Google Cloud SDK: https://cloud.google.com/sdk


Service account private key files
+++++++++++++++++++++++++++++++++

A service account private key file can be used to obtain credentials for a
service account. You can create a private key using the `Credentials page of the
Google Cloud Console`_. Once you have a private key you can either obtain
credentials one of two ways:

1. Set the ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable to the full
   path to your service account private key file

   .. code-block:: bash

        $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

   Then, use :ref:`application default credentials <application-default>`.
   :func:`default` checks for the ``GOOGLE_APPLICATION_CREDENTIALS``
   environment variable before all other checks, so this will always use the
   credentials you explicitly specify.

2. Use :meth:`service_account.Credentials.from_service_account_file
   <google.oauth2.service_account.Credentials.from_service_account_file>`::

        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(
            '/path/to/key.json')

        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/cloud-platform'])

.. warning:: Private keys must be kept secret. If you expose your private key it
    is recommended to revoke it immediately from the Google Cloud Console.

.. _Credentials page of the Google Cloud Console:
    https://console.cloud.google.com/apis/credentials

Compute Engine, Container Engine, and the App Engine flexible environment
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Applications running on `Compute Engine`_, `Container Engine`_, or the `App
Engine flexible environment`_ can obtain credentials provided by `Compute
Engine service accounts`_. When running on these platforms you can obtain
credentials for the service account one of two ways:

1. Use :ref:`application default credentials <application-default>`.
   :func:`default` will automatically detect if these credentials are available.

2. Use :class:`compute_engine.Credentials`::

        from google.auth import compute_engine

        credentials = compute_engine.Credentials()

.. _Compute Engine: https://cloud.google.com/compute
.. _Container Engine: https://cloud.google.com/container-engine
.. _App Engine flexible environment:
    https://cloud.google.com/appengine/docs/flexible/
.. _Compute Engine service accounts:
    https://cloud.google.com/compute/docs/access/service-accounts

The App Engine standard environment
+++++++++++++++++++++++++++++++++++

Applications running on the `App Engine standard environment`_ can obtain
credentials provided by the `App Engine App Identity API`_. You can obtain
credentials one of two ways:

1. Use :ref:`application default credentials <application-default>`.
   :func:`default` will automatically detect if these credentials are available.

2. Use :class:`app_engine.Credentials`::

        from google.auth import app_engine

        credentials = app_engine.Credentials()

In order to make authenticated requests in the App Engine environment using the
credentials and transports provided by this library, you need to follow a few
additional steps:

#. If you are using the :mod:`google.auth.transport.requests` transport, vendor
   in the `requests-toolbelt`_ library into your app, and enable the App Engine
   monkeypatch. Refer `App Engine documentation`_ for more details on this.
#. To make HTTPS calls, enable the ``ssl`` library for your app by adding the
   following configuration to the ``app.yaml`` file::

        libraries:
        - name: ssl
          version: latest

#. Enable billing for your App Engine project. Then enable socket support for
   your app. This can be achieved by setting an environment variable in the
   ``app.yaml`` file::

        env_variables:
          GAE_USE_SOCKETS_HTTPLIB : 'true'

.. _App Engine standard environment:
    https://cloud.google.com/appengine/docs/python
.. _App Engine App Identity API:
    https://cloud.google.com/appengine/docs/python/appidentity/
.. _requests-toolbelt:
    https://toolbelt.readthedocs.io/en/latest/
.. _App Engine documentation:
    https://cloud.google.com/appengine/docs/standard/python/issue-requests

User credentials
++++++++++++++++

User credentials are typically obtained via `OAuth 2.0`_. This library does not
provide any direct support for *obtaining* user credentials, however, you can
use user credentials with this library. You can use libraries such as
`oauthlib`_ to obtain the access token. After you have an access token, you
can create a :class:`google.oauth2.credentials.Credentials` instance::

    import google.oauth2.credentials

    credentials = google.oauth2.credentials.Credentials(
        'access_token')

If you obtain a refresh token, you can also specify the refresh token and token
URI to allow the credentials to be automatically refreshed::

    credentials = google.oauth2.credentials.Credentials(
        'access_token',
        refresh_token='refresh_token',
        token_uri='token_uri',
        client_id='client_id',
        client_secret='client_secret')


There is a separate library, `google-auth-oauthlib`_, that has some helpers
for integrating with `requests-oauthlib`_ to provide support for obtaining
user credentials. You can use
:func:`google_auth_oauthlib.helpers.credentials_from_session` to obtain
:class:`google.oauth2.credentials.Credentials` from a 
:class:`requests_oauthlib.OAuth2Session` as above::

    from google_auth_oauthlib.helpers import credentials_from_session

    google_auth_credentials = credentials_from_session(oauth2session)

You can also use :class:`google_auth_oauthlib.flow.Flow` to perform the OAuth
2.0 Authorization Grant Flow to obtain credentials using `requests-oauthlib`_.

.. _OAuth 2.0:
    https://developers.google.com/identity/protocols/OAuth2
.. _oauthlib:
    https://oauthlib.readthedocs.io/en/latest/
.. _google-auth-oauthlib:
    https://pypi.python.org/pypi/google-auth-oauthlib
.. _requests-oauthlib:
    https://requests-oauthlib.readthedocs.io/en/latest/

Impersonated credentials
++++++++++++++++++++++++

Impersonated Credentials allows one set of credentials issued to a user or service account
to impersonate another.  The target service account must grant the source credential
the "Service Account Token Creator" IAM role::

    from google.auth import impersonated_credentials

    target_scopes = ['https://www.googleapis.com/auth/devstorage.read_only']
    source_credentials = service_account.Credentials.from_service_account_file(
        '/path/to/svc_account.json',
        scopes=target_scopes)

    target_credentials = impersonated_credentials.Credentials(
        source_credentials=source_credentials,
        target_principal='impersonated-account@_project_.iam.gserviceaccount.com',
        target_scopes=target_scopes,
        lifetime=500)
    client = storage.Client(credentials=target_credentials)
    buckets = client.list_buckets(project='your_project')
    for bucket in buckets:
        print bucket.name


In the example above `source_credentials` does not have direct access to list buckets
in the target project.  Using `ImpersonatedCredentials` will allow the source_credentials
to assume the identity of a target_principal that does have access

Making authenticated requests
-----------------------------

Once you have credentials you can attach them to a *transport*. You can then
use this transport to make authenticated requests to APIs. google-auth supports
several different transports. Typically, it's up to your application or an
opinionated client library to decide which transport to use.

Requests
++++++++

The recommended HTTP transport is :mod:`google.auth.transport.requests` which
uses the `Requests`_ library. To make authenticated requests using Requests
you use a custom `Session`_ object::

    from google.auth.transport.requests import AuthorizedSession

    authed_session = AuthorizedSession(credentials)

    response = authed_session.get(
        'https://www.googleapis.com/storage/v1/b')

.. _Requests: http://docs.python-requests.org/en/master/
.. _Session: http://docs.python-requests.org/en/master/user/advanced/#session-objects

urllib3
+++++++

:mod:`urllib3` is the underlying HTTP library used by Requests and can also be
used with google-auth. urllib3's interface isn't as high-level as Requests but
it can be useful in situations where you need more control over how HTTP
requests are made. To make authenticated requests using urllib3 create an
instance of :class:`google.auth.transport.urllib3.AuthorizedHttp`::

    from google.auth.transport.urllib3 import AuthorizedHttp

    authed_http = AuthorizedHttp(credentials)

    response = authed_http.request(
        'GET', 'https://www.googleapis.com/storage/v1/b')

You can also construct your own :class:`urllib3.PoolManager` instance and pass
it to :class:`~google.auth.transport.urllib3.AuthorizedHttp`::

    import urllib3

    http = urllib3.PoolManager()
    authed_http = AuthorizedHttp(credentials, http)

gRPC
++++

`gRPC`_ is an RPC framework that uses `Protocol Buffers`_ over `HTTP 2.0`_.
google-auth can provide `Call Credentials`_ for gRPC. The easiest way to do
this is to use google-auth to create the gRPC channel::

    import google.auth.transport.grpc
    import google.auth.transport.requests

    http_request = google.auth.transport.requests.Request()

    channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, 'pubsub.googleapis.com:443')

.. note:: Even though gRPC is its own transport, you still need to use one of
    the other HTTP transports with gRPC. The reason is that most credential
    types need to make HTTP requests in order to refresh their access token.
    The sample above uses the Requests transport, but any HTTP transport can
    be used. Additionally, if you know that your credentials do not need to
    make HTTP requests in order to refresh (as is the case with
    :class:`jwt.Credentials`) then you can specify ``None``.

Alternatively, you can create the channel yourself and use
:class:`google.auth.transport.grpc.AuthMetadataPlugin`::

    import grpc

    metadata_plugin = AuthMetadataPlugin(credentials, http_request)

    # Create a set of grpc.CallCredentials using the metadata plugin.
    google_auth_credentials = grpc.metadata_call_credentials(
        metadata_plugin)

    # Create SSL channel credentials.
    ssl_credentials = grpc.ssl_channel_credentials()

    # Combine the ssl credentials and the authorization credentials.
    composite_credentials = grpc.composite_channel_credentials(
        ssl_credentials, google_auth_credentials)

    channel = grpc.secure_channel(
        'pubsub.googleapis.com:443', composite_credentials)

You can use this channel to make a gRPC stub that makes authenticated requests
to a gRPC service::

    from google.pubsub.v1 import pubsub_pb2

    pubsub = pubsub_pb2.PublisherStub(channel)

    response = pubsub.ListTopics(
        pubsub_pb2.ListTopicsRequest(project='your-project'))


.. _gRPC: http://www.grpc.io/
.. _Protocol Buffers:
    https://developers.google.com/protocol-buffers/docs/overview
.. _HTTP 2.0:
    http://www.grpc.io/docs/guides/wire.html
.. _Call Credentials:
    http://www.grpc.io/docs/guides/auth.html
