Integration with Python logging module
--------------------------------------


It's possible to tie the Python :mod:`logging` module directly into Google Cloud Logging. To use it,
create a :class:`CloudLoggingHandler <google.cloud.logging.CloudLoggingHandler>` instance from your
Logging client.

.. code-block:: python

    >>> import logging
    >>> import google.cloud.logging # Don't conflict with standard logging
    >>> from google.cloud.logging.handlers import CloudLoggingHandler
    >>> client = google.cloud.logging.Client()
    >>> handler = CloudLoggingHandler(client)
    >>> cloud_logger = logging.getLogger('cloudLogger')
    >>> cloud_logger.setLevel(logging.INFO) # defaults to WARN
    >>> cloud_logger.addHandler(handler)
    >>> cloud_logger.error('bad news')

.. note::

    This handler by default uses an asynchronous transport that sends log entries on a background
     thread. However, the API call will still be made in the same process. For other transport
     options, see the transports section.

All logs will go to a single custom log, which defaults to "python". The name of the Python
logger will be included in the structured log entry under the "python_logger" field. You can
change it by providing a name to the handler:

.. code-block:: python

    >>> handler = CloudLoggingHandler(client, name="mycustomlog")

It is also possible to attach the handler to the root Python logger, so that for example a plain
`logging.warn` call would be sent to Cloud Logging, as well as any other loggers created. However,
you must avoid infinite recursion from the logging calls the client itself makes. A helper
method :meth:`setup_logging <google.cloud.logging.handlers.setup_logging>` is provided to configure
this automatically:

.. code-block:: python

    >>> import logging
    >>> import google.cloud.logging # Don't conflict with standard logging
    >>> from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging
    >>> client = google.cloud.logging.Client()
    >>> handler = CloudLoggingHandler(client)
    >>> logging.getLogger().setLevel(logging.INFO) # defaults to WARN
    >>> setup_logging(handler)
    >>> logging.error('bad news')

You can also exclude certain loggers:

.. code-block:: python

   >>> setup_logging(handler, excluded_loggers=('werkzeug',))



Python logging handler transports
==================================

The Python logging handler can use different transports. The default is
:class:`google.cloud.logging.handlers.BackgroundThreadTransport`.

 1. :class:`google.cloud.logging.handlers.BackgroundThreadTransport` this is the default. It writes
 entries on a background :class:`python.threading.Thread`.

 1. :class:`google.cloud.logging.handlers.SyncTransport` this handler does a direct API call on each
 logging statement to write the entry.
