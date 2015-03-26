``gcloud.storage`` API
======================

Connection / Authorization
--------------------------

- Inferred defaults used to create connection if none configured explicitly

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

- Declaratively set defaults one-by-one

  .. code-block:: python

   >>> storage.set_default_bucket(some_bucket)
   >>> storage.set_default_connection(connection)
   >>> storage.set_default_project(project)


Manage buckets
--------------

Create a new bucket

.. code-block:: python

   >>> from gcloud import storage
   >>> new_bucket = storage.create_bucket(bucket_name)

if you desire to be declarative, you may pass in a connection to
override the default

.. code-block:: python

   >>> new_bucket = storage.create_bucket(bucket_name, connection=connection)

.. note::
  All methods in the ``storage`` package accept ``connection`` as an optional
  parameter.

Retrieve an existing bucket

.. code-block:: python

   >>> existing_bucket = storage.get_bucket(bucket_name)

but if the bucket does not exist an exception will occur

.. code-block:: python

   >>> existing_bucket = storage.get_bucket(bucket_name)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   gcloud.exceptions.NotFound: 404 Some Message

To get a null response instead of an exception, use
:func:`lookup_bucket <gcloud.storage.api.lookup_bucket>`

.. code-block:: python

   >>> non_existent = storage.lookup_bucket(bucket_name)
   >>> print non_existent
   None

To retrieve multiple buckets in a single request

.. code-block:: python

   >>> bucket1, bucket2, bucket3 = storage.get_buckets('bucket-name1',
   ...                                                 'bucket-name2',
   ...                                                 'bucket-name3')

This is equivalent to

.. code-block:: python

   >>> with storage.Batch():
   ...     bucket1 = storage.get_bucket('bucket-name1')
   ...     bucket2 = storage.get_bucket('bucket-name2')
   ...     bucket3 = storage.get_bucket('bucket-name3')

To list all buckets associated to the default project

.. code-block:: python

   >>> for bucket in storage.list_buckets():
   ...     print bucket
   <Bucket: foo>
   <Bucket: bar>
   <Bucket: baz>

or to use a project other than the default

.. code-block:: python

   >>> for bucket in storage.list_buckets('some-project'):
   ...     print bucket

To limit the list of buckets returned,
:func:`list_buckets() <gcloud.storage.list_buckets>` accepts optional
arguments

.. code-block:: python

   >>> bucket_iterator = storage.list_buckets(max_results=2,
   ...                                        page_token='next-bucket-name',
   ...                                        prefix='foo',
   ...                                        projection='noAcl',
   ...                                        fields=None)
   >>> for bucket in bucket_iterator:
   ...     print bucket

See the `buckets list`_ documentation for details.

.. _buckets list: https://cloud.google.com/storage/docs/json_api/v1/buckets/list

To delete a bucket

.. code-block:: python

   >>> storage.delete_bucket(bucket_name)

.. warning::
  Deleting a bucket should happen very infrequently. Be careful that you
  actually mean to delete the bucket.

.. note::
  We use the term blob interchangeably with "object" when referring to the
  API. The Google Cloud Storage documentation use object, but we use ``blob``
  instead to avoid confusion with the Python builtin ``object``.

In the case that the bucket has existing blobs, the backend
will return a `409 conflict`_ and raise

.. code-block:: python

   >>> storage.delete_bucket(bucket_name)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   gcloud.exceptions.Conflict: 409 Some Message

this can be addressed by using the ``force`` keyword

   >>> storage.delete_bucket(bucket_name, force=True)

Even using ``force=True`` will fail if the bucket contains more than 256
blobs. In this case, the blobs should be deleted manually first.

.. _409 conflict: http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error

Working with Buckets
--------------------

To create a bucket object directly

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

By default, just constructing a :class:`Bucket <gcloud.storage.bucket.Bucket>`
does not load any of the associated bucket metadata. To load all bucket
properties

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
``eager`` keyword

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
   >>> bucket.storage_class = 'DURABLE_REDUCED_AVAILABILITY'
   >>> bucket.versioning_enabled = True
   >>> bucket.website = {
   ...     'mainPageSuffix': 'index.html',
   ...     'notFoundPage': '404.html',
   ... }

In general, many of these properties are optional and will not need to be
used (or changed from the defaults).

In addition, a bucket has several read-only properties

.. code-block:: python

   >>> bucket.etag
   u'CAI='
   >>> bucket.id
   u'bucket-name'
   >>> bucket.metageneration
   2L
   >>> bucket.name
   u'bucket-name'
   >>> bucket.owner
   {u'entity': u'project-owners-111111'}
   >>> bucket.project_number
   u'111111'
   >>> bucket.self_link
   u'https://www.googleapis.com/storage/v1/b/bucket-name'
   >>> bucket.time_created
   u'2015-01-01T12:00:00.000Z'

See `buckets`_ specification for more details.

Other data -- namely `access control`_ data -- is associated with buckets,
but is handled through ``Bucket.acl``.

.. _buckets: https://cloud.google.com/storage/docs/json_api/v1/buckets
.. _access control: https://cloud.google.com/storage/docs/access-control

.. note::
  **BREAKING THE FOURTH WALL**: Note that ``storage.buckets.update`` is
  absent. This doesn't seem necessary to implement given the presence of
  ``patch``.

Manage Blobs
------------

Interacting with blobs requires an associated bucket. Either methods on an
explicit :class:`Bucket <gcloud.storage.bucket.Bucket>` instance can be used
or the default bucket can be used via methods in the ``storage`` package.

To retrieve a blob with a bucket

.. code-block:: python

   >>> bucket.get_blob('blob-name')
   <Blob: bucket-name, blob-name>

or from the package via the default bucket

.. code-block:: python

   >>> storage.get_blob('blob-name')
   <Blob: default-bucket-name, blob-name>

Simply calling ``get_blob`` will not actually retrieve the contents stored
for the given blob. Instead, it retrieves the metadata associated with
the blob.

For the remainder of this section we will just illustrate the methods
on :class:`Bucket <gcloud.storage.bucket.Bucket>`. For each such method,
an equivalent function is defined in the ``storage`` package and each
such function relies on the default bucket.

To retrieve multiple blobs in a single request

.. code-block:: python

   >>> blob1, blob2, blob3 = bucket.get_blobs('blob-name1',
   ...                                        'blob-name2',
   ...                                        'blob-name3')

This is equivalent to

.. code-block:: python

   >>> with storage.Batch():
   ...     blob1 = bucket.get_blob('blob-name1')
   ...     blob2 = bucket.get_blob('blob-name2')
   ...     blob3 = bucket.get_blob('blob-name3')

however, recall that if ``bucket`` has a ``connection`` explicitly bound
to it, the ``bucket.get_blob`` requests will be executed individually
rather than as part of the batch.

To list all blobs in a bucket

.. code-block:: python

   >>> for blob in bucket.list_blobs():
   ...     print blob
   <Blob: bucket-name, blob-name1>
   <Blob: bucket-name, blob-name2>
   <Blob: bucket-name, blob-name3>

.. warning::
  In a production application, a typical bucket may very likely have thousands
  or even millions of blobs. Iterating through all of them in such an
  application is a very bad idea.

To limit the list of blobs returned,
:meth:`list_blobs() <gcloud.storage.Bucket.list_blobs>` accepts optional
arguments

.. code-block:: python

   >>> blob_iterator = bucket.list_blobs(max_results=2,
   ...                                   page_token='next-blob-name',
   ...                                   prefix='foo',
   ...                                   delimiter='/',
   ...                                   versions=True,
   ...                                   projection='noAcl',
   ...                                   fields=None)
   >>> for blob in blob_iterator:
   ...     print blob

See the `objects list`_ documentation for details.

.. _objects list: https://cloud.google.com/storage/docs/json_api/v1/objects/list

To delete a blob

.. code-block:: python

   >>> bucket.delete_blob(blob_name)

As with retrieving, you may also delete multiple blobs in a single request

.. code-block:: python

   >>> bucket.delete_blobs('blob-name1', 'blob-name2', 'blob-name3')

This is equivalent to

.. code-block:: python

   >>> with storage.Batch():
   ...     bucket.delete_blob('blob-name1')
   ...     bucket.delete_blob('blob-name2')
   ...     bucket.delete_blob('blob-name3')

To copy an existing blob to a new location, potentially even in
a new bucket

.. code-block:: python

   >>> new_blob = bucket.copy_blob(blob, new_bucket, new_name='new-blob-name')

To compose multiple blobs together

.. code-block:: python

   >>> blob1, blob2 = bucket.get_blobs('blob-name1', 'blob-name2')
   >>> new_blob = bucket.compose('composed-blob', parts=[blob1, blob2])

To upload and download blob data, :class:`Blob <gcloud.storage.blob.Blob>`
objects should be used directly.

Working with Blobs
------------------

To create a blob object directly

.. code-block:: python

   >>> blob = storage.Blob('blob-name', bucket=bucket)
   >>> blob.exists()
   False
   >>> blob.create()
   >>> blob.exists()
   True
   >>> blob
   <Blob: bucket-name, blob-name>

If no ``bucket`` is provided, the default bucket will be used

.. code-block:: python

   >>> storage.Blob('blob-name')
   <Blob: default-bucket-name, blob-name>

By default, just constructing a :class:`Blob <gcloud.storage.blob.Blob>`
does not load any of the associated blob metadata. To load all blob
properties

.. code-block:: python

   >>> blob = storage.Blob('blob-name')
   >>> print blob.last_sync
   None
   >>> blob.properties
   {}
   >>> blob.reload()
   >>> blob.last_sync
   datetime.datetime(2015, 1, 1, 12, 0)
   >>> blob.properties
   {u'bucket': u'default-bucket-name',
    u'contentType': u'text/plain',
    ...}
   >>> blob.acl.loaded
   False
   >>> blob.acl.reload()
   >>> blob.acl.loaded
   True
   >>> blob.acl.entities
   {'project-editors-111111': <ACL Entity: project-editors-111111 (OWNER)>,
    'project-owners-111111': <ACL Entity: project-owners-111111 (OWNER)>,
    'project-viewers-111111': <ACL Entity: project-viewers-111111 (READER)>,
    'user-01234': <ACL Entity: user-01234 (OWNER)>}

Instead of calling
:meth:`Blob.reload() <gcloud.storage.blob.Blob.reload>` and
:meth:`ObjectACL.reload() <gcloud.storage.acl.ObjectACL.reload>`, you
can load the properties when the object is instantiated by using the
``eager`` keyword

.. code-block:: python

   >>> blob = storage.Blob('blob-name')
   >>> blob.last_sync
   datetime.datetime(2015, 1, 1, 12, 0)
   >>> blob.acl.loaded
   True

To delete a blob

.. code-block:: python

   >>> blob.delete()

To generate a signed URL for temporary privileged access to the
contents of a blob

.. code-block:: python

   >>> expiration_seconds = 600
   >>> signed_url = blob.generate_signed_url(expiration_seconds)

To make updates to the blob use
:meth:`Blob.patch() <gcloud.storage.blob.Blob.patch>`

.. code-block:: python

   >>> blob.versioning_enabled = True
   >>> blob.patch()

If there are no updates to send, an exception will occur

.. code-block:: python

   >>> blob.patch()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: No updates to send.

In total, the properties that can be updated are

.. code-block:: python

   >>> blob.cache_control = 'private, max-age=0, no-cache'
   >>> blob.content_disposition = 'Attachment; filename=example.html'
   >>> blob.content_encoding = 'gzip'
   >>> blob.content_language = 'en-US'
   >>> blob.content_type = 'text/plain'
   >>> blob.crc32c = u'z8SuHQ=='  # crc32-c of "foo"
   >>> blob.md5_hash = u'rL0Y20zC+Fzt72VPzMSk2A=='  # md5 of "foo"
   >>> blob.metadata = {'foo': 'bar', 'baz': 'qux'}

.. note::
  **BREAKING THE FOURTH WALL**: Why are ``crc32c`` and ``md5_hash`` writable?

In general, many of these properties are optional and will not need to be
used (or changed from the defaults).

In addition, a blob has several read-only properties

.. code-block:: python

   >>> blob.bucket
   <Bucket: bucket-name>
   >>> blob.component_count
   1
   >>> blob.etag
   u'CNiOr665xcQCEAE='
   >>> blob.generation
   12345L
   >>> blob.id
   u'bucket-name/blob-name/12345'
   >>> blob.media_link
   u'https://www.googleapis.com/download/storage/v1/b/bucket-name/o/blob-name?generation=12345&alt=media'
   >>> blob.metageneration
   1L
   >>> blob.name
   'blob-name'
   >>> blob.owner
   {u'entity': u'user-01234',
    u'entityId': u'01234'}
   >>> blob.self_link
   u'https://www.googleapis.com/storage/v1/b/bucket-name/o/blob-name'
   >>> blob.size
   3L
   >>> blob.storage_class
   u'STANDARD'
   >>> print blob.time_deleted
   None
   >>> blob.updated
   u'2015-01-01T12:00:00.000Z'

See `objects`_ specification for more details.

Other data -- namely `access control`_ data -- is associated with blobs,
but is handled through ``Blob.acl``.

.. _objects: https://cloud.google.com/storage/docs/json_api/v1/objects

Working with Blob Data
----------------------

The most important use of a blob is not accessing and updating the metadata,
it is storing data in the cloud (hence Cloud Storage).

To upload string data into a blob

  .. code-block:: python

   >>> blob.upload_from_string('foo')

If the data has a known content-type, set it on the blob before
uploading:

  .. code-block:: python

   >>> blob.content_type = 'application/zip'
   >>> blob.upload_from_string('foo')

To upload instead from a file

  .. code-block:: python

   >>> blob.upload_from_filename('/path/on/local/machine.file')

To download blob data into a string

  .. code-block:: python

   >>> blob_contents = blob.download_as_string()

To download instead to a file

  .. code-block:: python

   >>> blob.download_to_filename('/path/on/local/machine.file')

Dealing with ACLs
-----------------

To do
