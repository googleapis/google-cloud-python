Cloud Storage in 10 seconds
===========================

Install the library
-------------------

The source code for the library
(and demo code)
lives on GitHub,
You can install the library quickly with ``pip``::

  $ pip install gcloud

Run the
`example script <https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/gcloud/storage/demo/demo.py>`_
included in the package::

  $ python -m gcloud.storage.demo

And that's it!
You should be walking through
a demonstration of using ``gcloud.storage``
to read and write data to Google Cloud Storage.

Try it yourself
---------------

You can interact with a demo dataset
in a Python interactive shell.

Start by importing the demo module
and instantiating the demo connection::

  >>> from gcloud.storage import demo
  >>> connection = demo.get_connection()

Once you have the connection,
you can create buckets and keys::

  >>> connection.get_all_buckets()
  [<Bucket: ...>, ...]
  >>> bucket = connection.create_bucket('my-new-bucket')
  >>> print bucket
  <Bucket: my-new-bucket>
  >>> key = bucket.new_key('my-test-file.txt')
  >>> print key
  <Key: my-new-bucket, my-test-file.txt>
  >>> key = key.set_contents_from_string('this is test content!')
  >>> print key.get_contents_as_string()
  'this is test content!'
  >>> print bucket.get_all_keys()
  [<Key: my-new-bucket, my-test-file.txt>]
  >>> key.delete()
  >>> bucket.delete()

.. note::
  The ``get_connection`` method is just a shortcut for::

  >>> from gcloud import storage
  >>> from gcloud.storage import demo
  >>> connection = storage.get_connection(
  >>>     demo.PROJECT_NAME, demo.CLIENT_EMAIL, demo.PRIVATE_KEY_PATH)

OK, that's it!
--------------

And you can always check out
the :doc:`storage-api`.
