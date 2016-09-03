Using the API
=============


Authentication and Configuration
--------------------------------

- For an overview of authentication in ``google-cloud-python``,
  see :doc:`gcloud-auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd like
  to interact with. If you are Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`Client <google.cloud.error_reporting.client.Client>`

  .. doctest::

     >>> from google.cloud import error_reporting
     >>> client = error_reporting.Client()

  or pass in ``credentials`` and ``project`` explicitly

  .. doctest::

     >>> from google.cloud import error_reporting
     >>> client = error_reporting.Client(project='my-project', credentials=creds)

  Error Reporting associates errors with a service, which is an identifier for an executable,
  App Engine service, or job. The default service is "python", but a default can be specified
  for the client on construction time. You can also optionally specify a version for that service,
  which defaults to "default."


    .. doctest::

       >>> from google.cloud import error_reporting
       >>> client = error_reporting.Client(project='my-project',
       ...                                 service="login_service",
       ...                                 version="0.1.0")

Reporting an exception
-----------------------

Report a stacktrace to Stackdriver Error Reporting after an exception

.. doctest::

   >>> from google.cloud import error_reporting
   >>> client = error_reporting.Client()
   >>> try:
   >>>     raise NameError
   >>> except Exception:
   >>>     client.report_exception()


By default, the client will report the error using the service specified in the client's
constructor, or the default service of "python".

The user and HTTP context can also be included in the exception. The HTTP context
can be constructed using :class:`google.cloud.error_reporting.HTTPContext`. This will
be used by Stackdriver Error Reporting to help group exceptions.

.. doctest::

   >>> from google.cloud import error_reporting
   >>> client = error_reporting.Client()
   >>> user = 'example@gmail.com'
   >>> http_context = HTTPContext(method='GET', url='/', userAgent='test agent',
   ...                            referrer='example.com', responseStatusCode=500,
   ...                            remote_ip='1.2.3.4')
   >>> try:
   >>>     raise NameError
   >>> except Exception:
   >>>     client.report_exception(http_context=http_context, user=user))

Reporting an error without an exception
-----------------------------------------

Errors can also be reported to Stackdriver Error Reporting outside the context of an exception.
The library will include the file path, function name, and line number of the location where the
error was reported.

.. doctest::

   >>> from google.cloud import error_reporting
   >>> client = error_reporting.Client()
   >>> error_reporting.report("Found an error!")

Similarly to reporting an exception, the user and HTTP context can be provided:

.. doctest::

   >>> from google.cloud import error_reporting
   >>> client = error_reporting.Client()
   >>> user = 'example@gmail.com'
   >>> http_context = HTTPContext(method='GET', url='/', userAgent='test agent',
   ...                            referrer='example.com', responseStatusCode=500,
   ...                            remote_ip='1.2.3.4')
   >>> error_reporting.report("Found an error!", http_context=http_context, user=user))
