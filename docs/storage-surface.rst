``gcloud.storage`` API
======================

Connection / Authorization
--------------------------

- Inferred defaults used to create connection if none configured explicitly:

  - credentials (derived from GAE / GCE environ if present).

  - ``project`` (derived from GAE / GCE environ if present).

  - ``bucket`` (derived from GAE / GCE environ if present).

- By calling methods which require authentication

  .. code-block:: python

   >>> from gcloud import storage
   >>> bucket = storage.get_bucket('my-bucket')

  the default connection "just works" out of the box and will be lazily
  loaded and stored after the first use.

- Set defaults in a declarative fashion

  .. code-block:: python

   >>> storage.set_defaults()

  or instead of using implicit behavior, pass in defaults

  .. code-block:: python

   >>> storage.set_defaults(connection=connection, project='some-project')
   ...                      bucket=some_bucket)

  though not all are needed

  .. code-block:: python

   >>> storage.set_defaults(project='some-project', bucket=some_bucket)

- Set defaults one-by-one

  .. code-block:: python

   >>> storage.set_default_bucket(some_bucket)
   >>> storage.set_default_connection(connection)
   >>> storage.set_default_project(project)


Manage buckets
--------------

Create a new bucket:

.. code-block:: python

   >>> from gcloud import storage
   >>> new_bucket = storage.create_bucket(bucket_name)

if you desire to be declarative, you may pass in a connection to
override the default:

.. code-block:: python

   >>> new_bucket = storage.create_bucket(bucket_name, connection=connection)

Retrieve an existing bucket:

.. code-block:: python

   >>> existing_bucket = storage.get_bucket(bucket_name)

but if the bucket does not exist an exception will occur

.. code-block:: python

   >>> existing_bucket = storage.get_bucket(bucket_name)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   gcloud.exceptions.NotFound: 404 Some Message

To get a null response instead of an exception, use
:func:`lookup_bucket <gcloud.storage.api.lookup_bucket>`:

.. code-block:: python

   >>> non_existent = storage.lookup_bucket(bucket_name)
   >>> print non_existent
   None

To list all buckets:

.. code-block:: python

   >>> for bucket in storage.get_buckets():
   ...     print bucket
   <Bucket: foo>
   <Bucket: bar>
   <Bucket: baz>

or to use a project other than the default

.. code-block:: python

   >>> for bucket in storage.get_buckets('some-project'):
   ...     print bucket

To limit the list of buckets returned,
:func:`get_buckets() <gcloud.storage.get_buckets>` accepts optional
arguments

.. code-block:: python

   >>> bucket_iterator = storage.get_buckets(max_results=2,
   ...                                       page_token='next-bucket-name',
   ...                                       prefix='foo',
   ...                                       projection='noAcl',
   ...                                       fields=None)
   >>> for bucket in bucket_iterator:
   ...     print bucket

See the `buckets list`_ documenation for details.

.. _buckets list: https://cloud.google.com/storage/docs/json_api/v1/buckets/list

To delete a bucket

.. code-block:: python

   >>> storage.delete_bucket(bucket_name)

.. note::
  Deleting a bucket should happen very infrequently. Be careful that you
  actually mean to delete the bucket.

In the case that the bucket has existing objects (``Blob`` here), the backend
will return a `409 conflict`_ and raise

.. code-block:: python

   >>> storage.delete_bucket(bucket_name)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   gcloud.exceptions.Conflict: 409 Some Message

this can be addressed by using the ``force`` keyword:

   >>> storage.delete_bucket(bucket_name, force=True)

This too will fail if the bucket contains more than 256 blobs.
In this case, the blobs should be deleted manually first.

.. _409 conflict: http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error

Working with Buckets
--------------------

To create a bucket directly

.. code-block:: python

   >>> bucket = storage.Bucket('bucket-name')
   >>> bucket.exists()
   False
   >>> bucket.create()
   >>> bucket.exists()
   True

You can also use an explicit connection

.. code-block:: python

   >>> bucket = storage.Bucket('bucket-name', connection=connection)

.. note::
  An explicitly passed connection will be bound to the ``bucket`` and
  all objects associated with the bucket. This means that within a batch of
  updates, the ``connection`` will be used to make the request instead of
  the batch.

To load all bucket properties

.. code-block:: python

   >>> bucket = storage.Bucket('bucket-name')
   >>> print bucket.last_sync
   None
   >>> bucket.properties
   {}
   >>> bucket.reload()
   >>> bucket.last_sync
   datetime.datetime(2015, 1, 1, 12, 0)
   >>> bucket.properties
   {u'etag': u'CAE=',
    u'id': u'bucket-name',
    ...}
   >>> bucket.acl.loaded
   False
   >>> bucket.acl.reload()
   >>> bucket.acl.loaded
   True
   >>> bucket.acl.entities
   {'project-editors-111111': <ACL Entity: project-editors-111111 (OWNER)>,
    'project-owners-111111': <ACL Entity: project-owners-111111 (OWNER)>,
    'project-viewers-111111': <ACL Entity: project-viewers-111111 (READER)>,
    'user-01234': <ACL Entity: user-01234 (OWNER)>}

Instead of calling
:meth:`Bucket.reload() <gcloud.storage.bucket.Bucket.reload>` and
:meth:`BucketACL.reload() <gcloud.storage.acl.BucketACL.reload>`, you
can load the properties when the object is instantiated by using the
``eager`` keyword:

.. code-block:: python

   >>> bucket = storage.Bucket('bucket-name', eager=True)
   >>> bucket.last_sync
   datetime.datetime(2015, 1, 1, 12, 0)
   >>> bucket.acl.loaded
   True

To delete a bucket

.. code-block:: python

   >>> bucket.delete()

or

.. code-block:: python

   >>> bucket.delete(force=True)

as above.

To make updates to the bucket use
:meth:`Bucket.patch() <gcloud.storage.bucket.Bucket.patch>`

.. code-block:: python

   >>> bucket.versioning_enabled = True
   >>> bucket.patch()

If there are no updates to send, an exception will occur

.. code-block:: python

   >>> bucket.patch()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: No updates to send.

In total, the properties that can be updated are

.. code-block:: python

   >>> bucket.cors = [
   ...     {
   ...       'origin': ['http://example.appspot.com'],
   ...       'responseHeader': ['Content-Type'],
   ...       'method': ['GET', 'HEAD', 'DELETE'],
   ...       'maxAgeSeconds': 3600,
   ...     }
   ... ]
   >>> bucket.lifecycle = [
   ...     {
   ...         'action': {'type': 'Delete'},
   ...         'condition': {'age': 365},
   ...     },
   ... ]
   >>> bucket.location = 'ASIA'
   >>> bucket.logging = {
   ...     'logBucket': 'bucket-name',
   ...     'logObjectPrefix': 'foo/',
   ... }
   >>> bucket.versioning_enabled = True
   >>> bucket.website = {
   ...     'mainPageSuffix': 'index.html',
   ...     'notFoundPage': '404.html',
   ... }
   >>> bucket.storage_class = 'DURABLE_REDUCED_AVAILABILITY'

See `buckets`_ specification for more details. In general, many of these
properties are optional and will not need to be used (or changed from the
defaults).

Other data -- namely `access control`_ -- is associated with buckets, but
this data is handled through ``Bucket.acl``.

.. _buckets: https://cloud.google.com/storage/docs/json_api/v1/buckets
.. _access control: https://cloud.google.com/storage/docs/access-control

Manage Blobs
------------

Interacting with blobs requires an associated bucket.

To retrieve a blob, a bucket can be used directly

.. code-block:: python

   >>> bucket.get_blob('blob-name')
   <Blob: bucket-name, blob-name>

or the default bucket can be used implicitly

.. code-block:: python

   >>> storage.get_blob('blob-name')
   <Blob: default-bucket-name, blob-name>

Dealing with ACLs
-----------------

To do
