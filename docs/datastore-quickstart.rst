Get started in 10 seconds
-------------------------

.. warning::
  This will use a *shared* dataset,
  which means any data you save
  will be available to anyone.

  If you want to create your own dataset,
  follow the
  (pretty simple)
  instructions in the
  :doc:`datastore-getting-started`.

Install the library
~~~~~~~~~~~~~~~~~~~

The source code for the library
(and demo code)
lives on GitHub,
You can install the library quickly with ``pip``::

  $ pip install gcloud

Run the
`example script <https://github.com/jgeewax/gcloud/blob/master/datastore/demo/demo.py>`_
included in the package::

  $ python -m gcloud.datastore.demo

Try it yourself
~~~~~~~~~~~~~~~

Crack open a Python interactive shell::

  $ python  # or ipython

And play with the demo dataset::

  >>> from gcloud.datastore import demo
  >>> dataset = demo.get_dataset()

But once you have the dataset,
you can manipulate data in the datastore::

  >>> dataset.query('MyExampleKind').fetch()
  [<Entity{...}, ]
  >>> entity = dataset.entity('Person')
  >>> entity['name'] = 'Your name'
  >>> entity['age'] = 25
  >>> entity.save()
  >>> dataset.query('Person').fetch()
  [<Entity{...} {'name': 'Your name', 'age': 25}>]

The ``get_dataset`` method is just a shortcut for::

  >>> from gcloud import datastore
  >>> from gcloud.datastore import demo
  >>> dataset = datastore.get_dataset(
          demo.DATASET_ID, demo.CLIENT_EMAIL, demo.PRIVATE_KEY_PATH)
