Cloud Storage in 10 seconds
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the library
^^^^^^^^^^^^^^^^^^^

The source code for the library
(and demo code)
lives on GitHub,
You can install the library quickly with ``pip``::

  $ pip install gcloud

Run the demo
^^^^^^^^^^^^

In order to run the demo, you need to have registred an actual ``gcloud``
project and so you'll need to provide some environment variables to facilitate
authentication to your project:

  - ``GCLOUD_TESTS_PROJECT_ID``: Developers Console project ID (e.g.
    bamboo-shift-455).
  - ``GCLOUD_TESTS_DATASET_ID``: The name of the dataset your tests connect to.
    This is typically the same as ``GCLOUD_TESTS_PROJECT_ID``.
  - ``GOOGLE_APPLICATION_CREDENTIALS``: The path to a JSON key file;
    see ``regression/app_credentials.json.sample`` as an example. Such a file
    can be downloaded directly from the developer's console by clicking
    "Generate new JSON key". See private key
    `docs <https://cloud.google.com/storage/docs/authentication#generating-a-private-key>`__
    for more details.

Run the
`example script <https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/gcloud/storage/demo/demo.py>`_
included in the package::

  $ python -m gcloud.storage.demo

And that's it!
You should be walking through
a demonstration of using ``gcloud.storage``
to read and write data to Google Cloud Storage.

Try it yourself
^^^^^^^^^^^^^^^

You can interact with a demo dataset
in a Python interactive shell.

Start by importing the demo module
and instantiating the demo connection::

  >>> from gcloud.storage import demo
  >>> connection = demo.get_connection()

Once you have the connection,
you can create buckets and blobs::

  >>> from gcloud import storage
  >>> storage.get_all_buckets(connection)
  [<Bucket: ...>, ...]
  >>> bucket = connection.create_bucket('my-new-bucket')
  >>> print bucket
  <Bucket: my-new-bucket>
  >>> blob = bucket.new_blob('my-test-file.txt')
  >>> print blob
  <Blob: my-new-bucket, my-test-file.txt>
  >>> blob = blob.upload_from_string('this is test content!')
  >>> print blob.download_as_string()
  'this is test content!'
  >>> print bucket.get_all_blobs()
  [<Blob: my-new-bucket, my-test-file.txt>]
  >>> blob.delete()
  >>> bucket.delete()

.. note::
  The ``get_connection`` method is just a shortcut for::

  >>> from gcloud import storage
  >>> from gcloud.storage import demo
  >>> connection = storage.get_connection(demo.PROJECT_ID)

----
