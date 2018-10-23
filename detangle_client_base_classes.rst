De-tangling Client Base Classes
===============================

Survey client classes
---------------------

Figure out which client classes consume which base classes.


Autogen clients
~~~~~~~~~~~~~~~

These clients are auto-genereated, and do all API requests over gRPC:

- ``asset``
- ``automl``
- ``bigquery_datatransfer``
- ``container``
- ``dataproc``
- ``dlp``
- ``iot``
- ``kms``
- ``language``
- ``monitoring`` (handwritten ``query`` module uses only one client method).
- ``oslogin``
- ``redis``
- ``speech`` (client mixes in ``SpeechHelpers`` oddly)
- ``tasks``
- ``texttospeech``
- ``trace``
- ``videointelligence``
- ``vision``
- ``websecurityscanner``

None of them import from ``google.cloud.client``.


Manual GAPIC-only clients
~~~~~~~~~~~~~~~~~~~~~~~~~

These clients do all API requests over gRPC:

- ``bigtable``
- ``firestore``
- ``pubsub`` (``PublisherClient`` and ``SubscriberClient``).
- ``spanner``

Of these, the following still import from ``google.cloud.client``:

- ``bigtable``
- ``firestore``
- ``spanner``


HTTP-only clients
~~~~~~~~~~~~~~~~~

These clients do all API requests over HTTP:

- ``bigquery``
- ``dns``
- ``resource_manager``
- ``runtimeconfig``
- ``storage``
- ``translate``


Hybrid clients
~~~~~~~~~~~~~~

These clients allow selecting between gRPC and HTTP via an environment
variable, used to select which API wrapper to construct.

- ``datastore``
- ``error_reporting``
- ``logging``


Base Classes Defined
--------------------

``google.cloud.client._ClientFactoryMixin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Provides only ``from_service_account_json`` classmethod as a factory: it
  loads credentials from a service account file and delegates to the main
  class ctor with loaded credentials in ``**kwargs``.

- If subclasses define ``_SET_PROJECT``, copies project ID from the
  credentials into the ``**kwargs``. (This feature is only used by


``google.cloud.client.Client``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Mixes in ``_ClientFactoryMixin``.

- Ctor forces ``credentials`` to be ``google.auth.credentials.Credentials``,
  if passed.

- Ctor takes optional ``_http`` (eewwww!), which is expected to be a
  ``requests.Session`` workalike.

- IFF both ``credentials`` and ``_http`` are None, looks up default
  credentials using ``google.auth.default``.

- Allows subclasses to define ``SCOPE``, and uses it to wrap the passed
  or looked-up credentials using
  ``google.auth.credentials.with_scopes_if_required``

- Saves the passed-in ``_http`` to an ``_http_internal`` attribute, exposed
  as a read-only ``_http`` property.

- If not set, the ``_http`` property constructs a
  ``google.auth.transport.requests.AuthorizedSession`` using the client's
  credentials.


``google.cloud.client._ClientProjectMixin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ctor takes a ``project`` argument.  If not passed, attempts to look one
  up via its staticmethod helper, ``_determine_default``, and converts to
  text if needed (raising if conversion cannot be done text).
  
- The default implementation of ``_determine_default`` delegates to
  ``google.cloud._helpers._determine_default_project``.
  
- The ``datastore`` client overrides ``_determine_default`` to prefer the
  environment variable used by the Datstore emulator.


``google.cloud.client.ClientWithProject``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Derived from ``Client`` and ``_ClientProjectMixin``.

- Assigns ``_SET_PROJECT`` to ``True``.

- Ctor takes ``credentials``, ``project``, and ``_http``, and delegates
  to both base class ctors.



Analysis
--------

Client credentials
~~~~~~~~~~~~~~~~~~

- All clients need to be able to take credentials as a ctor argument.  If
  not passed, they need to be able *at some point before credentials are
  needed* to infer them from the environment.

- Some clients may not need to have explicit credentials.  E.g., the ``storage``
  client has a custom classmethod factory, ``create_anonymous_client``,
  which uses ``google.auth.credentials.AnonymousCredentials``.

- Eager construction / lookup of credentials in the ctor is probably the
  wrong thing, but does have the benefit of ensuring thread-saftey for
  credentials after construction of the client.

- In addition to using credentials to initialize their HTTP or GRPC
  transport wrapprs, some clients may need to use credentials for other
  purposes.  E.g., the ``storage`` client's credentials are used to create
  signed URLs providing temporary anonymous access to upload files to a
  bucket.

Client project ID
~~~~~~~~~~~~~~~~~

- All clients need to be able to take a project ID as a ctor argument.  If
  not passed, they need to be able *at some point before a project ID is
  needed* to infer it from the environment (or the credentials).
 
- Some clients may not need an explicit project ID.  E.g., that
  the ``storage`` client's ``create_anonymous_client`` passes a sentinel
  value for the project ID.  It's constructor also does a convoluted dance
  for the case that ``project`` is explicitly passed as ``None``, restoring
  that value after calling the base class' ``__init__``.

- Eager construction / lookup of the project ID in the ctor is probably the
  wrong thing, but does have the benefit of ensuring thread-saftey for
  the value after construction of the client.

- The patterns for inferring the project ID are convoluted, and maybe
  buggy (e.g., the known flakiness of the GCE metadata server).
  They also interact poorly with generalized support for API emulators (e.g.,
  the contortions in the ``datastore`` client to support the emulator's
  environment variable).

HTTP-based Clients
~~~~~~~~~~~~~~~~~~~

- Currently, HTTP-based clients hold / create an object which emulates the
  ``request.Session`` API, and make that object available to their connection
  instances (API wrappers) via their ``_http`` attribute.

- I believe it would be cleaner to have the instance passed to the connection
  objects' constructors, rather than having them use the attribute.

- The ``storage`` client contorts around the ``_http`` attribute in its
  ``test_batch`` unit tests:  get rid of that!

- In addition to its "normal" connection wrapper, the ``bigquery`` client
  passes its ``_http`` attribute to the "upload" objects used for loading
  table data to GCS in its ``load_table_from_file`` method.

- Clients which are passed on already-created ``requests.Session``-workalike
  should *not* need / require / infer credentials.

Hybrid Clients
~~~~~~~~~~~~~~

- The ``logging`` and ``datastore`` clients both follow a similar pattern
  for HTTP transport:  if GRPC is disabled via an environment variable or
  ctor arugument, they construct an API wrapper which expects to use their
  ``_connection`` attribute.  This means that the attribute has to be
  initialized, even in the case that GRPC is used.

- For the ``error_reporting`` client, if GRCP is disabled, it constructs its
  wrapper passing its project, credentials, and ``_http`` attributes.  The
  reason is that these values are used to initialize a ``logging`` client
  held by the wrapper.
