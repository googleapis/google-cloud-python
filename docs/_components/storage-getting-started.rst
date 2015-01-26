Getting started with Cloud Storage
==================================

This tutorial focuses on using ``gcloud`` to access
Google Cloud Storage.
We'll go through the basic concepts,
how to operate on buckets and blobs,
and how to handle access control,
among other things.

We're going to assume that you've already downloaded
and installed the library.

Creating a project
------------------

.. include:: _components/creating-a-project.rst

Enabling the API
----------------

Now that you created a project,
you need to **turn on** the Google Cloud Storage API.
This is sort of like telling Google
which services you intend to use for this project.

* **Click on APIs & Auth**
  on the left hand side,
  and scroll down to where it says
  "Google Cloud Storage JSON API".

* **Click the "Off" button**
  on the right side
  to turn it into an "On" button.

Enabling a service account
--------------------------

.. include:: _components/enabling-a-service-account.rst

Creating a connection
---------------------

The first step in accessing Cloud Storage
is to create a connection to the service::

  >>> from gcloud import storage
  >>> connection = storage.get_connection(project_name)

We're going to use this
:class:`connection <gcloud.storage.connection.Connection>` object
for the rest of this guide.

Creating a bucket
-----------------

Once you've established a connection to Cloud Storage,
the first thing you typically want to do is
create a new bucket.
A bucket is a container used to store
objects in Cloud Storage
(if you're familiar with S3,
buckets on Cloud Storage mean the same thing).
Think of each bucket as a single "disk drive",
where you can store lots of files on each.
How you organize your data is up to you,
but it's typical to group common data
in a single bucket.

Let's create a bucket:

  >>> bucket = connection.create_bucket('test')
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "gcloud/storage/connection.py", line 340, in create_bucket
      data={'name': bucket.name})
    File "gcloud/storage/connection.py", line 224, in api_request
      raise exceptions.ConnectionError(response, content)
  gcloud.storage.exceptions.ConnectionError: {'status': '409', 'alternate-protocol': '443:quic', 'content-length': '271', 'x-xss-protection': '1; mode=block', 'x-content-type-options': 'nosniff', 'expires': 'Sat, 15 Mar 2014 19:19:47 GMT', 'server': 'GSE', '-content-encoding': 'gzip', 'cache-control': 'private, max-age=0', 'date': 'Sat, 15 Mar 2014 19:19:47 GMT', 'x-frame-options': 'SAMEORIGIN', 'content-type': 'application/json; charset=UTF-8'}{
   "error": {
    "errors": [
     {
      "domain": "global",
      "reason": "conflict",
      "message": "Sorry, that name is not available. Please try a different one."
     }
    ],
    "code": 409,
    "message": "Sorry, that name is not available. Please try a different one."
   }
  }

**Whoops!**
It might be important to mention
that bucket names are like domain names:
it's one big namespace that we all share,
so you have to pick a bucket name that isn't already taken.

It's up to you to decide what a good name is,
let's assume that you found a unique name
and are ready to move on with your newly created bucket.

Storing data
------------

OK, so you have a bucket. Now what?
Cloud Storage is just an arbitrary data container,
so you can put whatever format of data you want.
The naming of your files is also arbitrary,
however the Cloud Storage online file browser
tries to make it feel a bit like a file system
by recognizing forward-slashes (``/``)
so if you want to group data into "directories",
you can do that.

The fundamental container for a file in Cloud Storage
is called an Object, however ``gcloud`` uses the term ``Blob``
to avoid confusion with the Python built-in ``object``.

If you want to set some data,
you just create a ``Blob`` inside your bucket
and store your data inside the blob::

  >>> blob = bucket.new_blob('greeting.txt')
  >>> blob.upload_from_string('Hello world!')

:func:`new_blob <gcloud.storage.bucket.Bucket.new_blob>`
creates a :class:`Blob <gcloud.storage.blob.Blob>` object locally
and
:func:`upload_from_string <gcloud.storage.blob.Blob.upload_from_string>`
allows you to put a string into the blob.

Now we can test if it worked::

  >>> blob = bucket.get_blob('greeting.txt')
  >>> print blob.download_as_string()
  Hello world!

What if you want to save the contents to a file?

  >>> blob.download_to_file('greetings.txt')

Then you can look at the file in a terminal::

  $ cat greetings.txt
  Hello world!

And what about when you're not dealing with text?
That's pretty simple too::

  >>> blob = bucket.new_blob('kitten.jpg')
  >>> blob.upload_from_filename('kitten.jpg')

And to test whether it worked?

  >>> blob = bucket.get_blob('kitten.jpg')
  >>> blob.download_to_file('kitten2.jpg')

and check if they are the same in a terminal::

  $ diff kitten.jpg kitten2.jpg

Notice that we're using
:func:`get_blob <gcloud.storage.bucket.Bucket.get_blob>`
to retrieve a blob we know exists remotely.
If the blob doesn't exist, it will return ``None``.

.. note:: ``get_blob`` is **not** retrieving the entire object's data.

If you want to "get-or-create" the blob
(that is, overwrite it if it already exists),
you can use :func:`new_blob <gcloud.storage.bucket.Bucket.new_blob>`.
However, keep in mind, the blob is not created
until you store some data inside of it.

If you want to check whether a blob exists,
you can use the ``in`` operator in Python::

  >>> print 'kitten.jpg' in bucket
  True
  >>> print 'does-not-exist' in bucket
  False

Accessing a bucket
------------------

If you already have a bucket,
use :func:`get_bucket <gcloud.storage.connection.Connection.get_bucket>`
to retrieve the bucket object::

  >>> bucket = connection.get_bucket('my-bucket')

If you want to get all the blobs in the bucket,
you can use
:func:`get_all_blobs <gcloud.storage.bucket.Bucket.get_all_blobs>`::

  >>> blobs = bucket.get_all_blobs()

However, if you're looking to iterate through the blobs,
you can use the bucket itself as an iterator::

  >>> for blob in bucket:
  ...   print blob

Deleting a bucket
-----------------

You can delete a bucket using the
:func:`delete_bucket <gcloud.storage.connection.Connection.delete_bucket>`
method::

  >>> connection.delete_bucket('my-bucket')

Remember, the bucket you're deleting needs to be empty,
otherwise you'll get an error.

If you have a full bucket, you can delete it this way::

  >>> bucket = connection.delete_bucket('my-bucket', force=True)

Listing available buckets
-------------------------

The :class:`Connection <gcloud.storage.connection.Connection>`
object itself is iterable,
so you can loop over it, or call ``list`` on it to get a list object::

  >>> for bucket in connection:
  ...   print bucket.name
  >>> print list(connection)

Managing access control
-----------------------

Cloud storage provides fine-grained access control
for both buckets and blobs.
`gcloud` tries to simplify access control
by working with entities and "grants".
On any ACL,
you get a reference to an entity,
and then either grant or revoke a specific access level.
Additionally, we provide two default entities:
all users, and all authenticated users.

For example, if you want to grant read access to all users on your bucket::

  >>> bucket.get_acl().all().grant_read()

For more detail on access control,
see :mod:`gcloud.storage.acl`.
