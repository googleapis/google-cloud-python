Type Marshaling
===============

Proto Plus provides a service that converts between protocol buffer objects
and native Python types (or the wrapper types provided by this library).

This allows native Python objects to be used in place of protocol buffer
messages where appropriate. In all cases, we return the native type, and are
liberal on what we accept.

Well-known types
----------------

The following types are currently handled by Proto Plus:

=================================== ======================= ========
Protocol buffer type                Python type             Nullable
=================================== ======================= ========
``google.protobuf.BoolValue``       ``bool``                     Yes
``google.protobuf.BytesValue``      ``bytes``                    Yes
``google.protobuf.DoubleValue``     ``float``                    Yes
``google.protobuf.Duration``        ``datetime.timedelta``         –
``google.protobuf.FloatValue``      ``float``                    Yes
``google.protobuf.Int32Value``      ``int``                      Yes
``google.protobuf.Int64Value``      ``int``                      Yes
``google.protobuf.StringValue``     ``str``                      Yes
``google.protobuf.Timestamp``       ``datetime.datetime``        Yes
``google.protobuf.UInt32Value``     ``int``                      Yes
``google.protobuf.UInt64Value``     ``int``                      Yes
=================================== ======================= ========

.. note::

    Protocol buffers include well-known types for ``Timestamp`` and
    ``Duration``, both of which have nanosecond precision. However, the
    Python ``datetime`` and ``timedelta`` objects have only microsecond
    precision.

    If you *write* a timestamp field using a Python ``datetime`` value,
    any existing nanosecond precision will be overwritten.


Wrapper types
-------------

Additionally, every :class:`~.Message` subclass is a wrapper class. The
creation of the class also creates the underlying protocol buffer class, and
this is registered to the marshal.

The underlying protocol buffer message class is accessible with the
:meth:`~.Message.pb` class method.
