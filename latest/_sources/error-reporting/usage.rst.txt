Stackdriver Error Reporting
===========================

.. toctree::
  :maxdepth: 2
  :hidden:

  client
  util

Installation
------------

Install the ``google-cloud-error-reporting`` library using ``pip``:

.. code-block:: console

    $ pip install google-cloud-error-reporting

Authentication and Configuration
--------------------------------

- For an overview of authentication in ``google-cloud-python``,
  see :doc:`/core/auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd like
  to interact with. If you are Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`Client <google.cloud.error_reporting.client.Client>`

  .. code-block:: python

     >>> from google.cloud import error_reporting
     >>> client = error_reporting.Client()

  or pass in ``credentials`` and ``project`` explicitly

  .. code-block:: python

     >>> from google.cloud import error_reporting
     >>> client = error_reporting.Client(project='my-project', credentials=creds)

  Error Reporting associates errors with a service, which is an identifier for an executable,
  App Engine service, or job. The default service is "python", but a default can be specified
  for the client on construction time. You can also optionally specify a version for that service,
  which defaults to "default."


    .. code-block:: python

       >>> from google.cloud import error_reporting
       >>> client = error_reporting.Client(project='my-project',
       ...                                 service="login_service",
       ...                                 version="0.1.0")

Reporting an exception
-----------------------

Report a stacktrace to Stackdriver Error Reporting after an exception

.. code-block:: python

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

.. code-block:: python

   >>> from google.cloud import error_reporting
   >>> client = error_reporting.Client()
   >>> user = 'example@gmail.com'
   >>> http_context = error_reporting.HTTPContext(
   ...     method='GET', url='/', user_agent='test agent',
   ...     referrer='example.com', response_status_code=500,
   ...     remote_ip='1.2.3.4')
   >>> try:
   >>>     raise NameError
   >>> except Exception:
   >>>     client.report_exception(http_context=http_context, user=user))

An automatic helper to build the HTTP Context from a Flask (Werkzeug) request
object is provided.

 .. code-block:: python

    >>> from google.cloud.error_reporting import build_flask_context
    >>> @app.errorhandler(HTTPException)
    ... def handle_error(exc):
    ...     client.report_exception(
    ...         http_context=build_flask_context(request))
    ...     # rest of error response code here


Reporting an error without an exception
-----------------------------------------

Errors can also be reported to Stackdriver Error Reporting outside the context of an exception.
The library will include the file path, function name, and line number of the location where the
error was reported.

.. code-block:: python

   >>> from google.cloud import error_reporting
   >>> client = error_reporting.Client()
   >>> error_reporting.report("Found an error!")

Similarly to reporting an exception, the user and HTTP context can be provided:

.. code-block:: python

   >>> from google.cloud import error_reporting
   >>> client = error_reporting.Client()
   >>> user = 'example@gmail.com'
   >>> http_context = error_reporting.HTTPContext(
   ...     method='GET', url='/', user_agent='test agent',
   ...     referrer='example.com', response_status_code=500,
   ...     remote_ip='1.2.3.4')
   >>> error_reporting.report("Found an error!", http_context=http_context, user=user))

Changelog
---------

For a list of all ``google-cloud-error-reporting`` releases:

.. toctree::
  :maxdepth: 2

  changelog
