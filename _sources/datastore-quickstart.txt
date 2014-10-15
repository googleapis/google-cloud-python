Cloud Datastore in 10 seconds
=============================

.. note::
  This will use a **shared** dataset,
  which means any data you save
  will be available to anyone.
  If you want to create your own dataset,
  follow the
  (pretty simple)
  instructions in the
  :doc:`datastore-getting-started`.

Install the library
-------------------

The source code for the library
(and demo code)
lives on GitHub,
You can install the library quickly with ``pip``::

  $ pip install gcloud

Run the
`example script <https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/gcloud/datastore/demo/demo.py>`_
included in the package::

  $ python -m gcloud.datastore.demo

And that's it!
You just read and wrote a bunch of data
to the Cloud Datastore.

Try it yourself
---------------

You can interact with a demo dataset
in a Python interactive shell.

Start by importing the demo module
and instantiating the demo dataset::

  >>> from gcloud.datastore import demo
  >>> dataset = demo.get_dataset()

Once you have the dataset,
you can create entities and save them::

  >>> dataset.query('MyExampleKind').fetch()
  [<Entity{...}, ]
  >>> entity = dataset.entity('Person')
  >>> entity['name'] = 'Your name'
  >>> entity['age'] = 25
  >>> entity.save()
  >>> dataset.query('Person').fetch()
  [<Entity{...} {'name': 'Your name', 'age': 25}>]

.. note::
  The ``get_dataset`` method is just a shortcut for::

  >>> from gcloud import datastore
  >>> from gcloud.datastore import demo
  >>> dataset = datastore.get_dataset(
  >>>     demo.DATASET_ID, demo.CLIENT_EMAIL, demo.PRIVATE_KEY_PATH)

OK, that's it!
--------------

Next,
take a look at the :doc:`datastore-getting-started`
to see how to create your own project and dataset.

And you can always check out
the :doc:`datastore-api`.
