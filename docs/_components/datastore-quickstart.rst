Cloud Datastore in 10 seconds
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
`example script <https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/gcloud/datastore/demo/demo.py>`_
included in the package::

  $ python -m gcloud.datastore.demo

And that's it!
You just read and wrote a bunch of data
to the Cloud Datastore.

Try it yourself
^^^^^^^^^^^^^^^

You can interact with a demo dataset
in a Python interactive shell.

Start by importing the demo module
and initializing the demo settings::

  >>> from gcloud.datastore import demo
  >>> demo.initialize()

Once you have initialized,
you can create entities and save them::

  >>> from gcloud import datastore
  >>> entity = datastore.Entity(key=datastore.Key('Person'))
  >>> entity['name'] = 'Your name'
  >>> entity['age'] = 25
  >>> entity.save()
  >>> list(datastore.Query(kind='Person').fetch())
  [<Entity{...} {'name': 'Your name', 'age': 25}>]

----
