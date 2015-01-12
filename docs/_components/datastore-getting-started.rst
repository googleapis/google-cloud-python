Getting started with Cloud Datastore
====================================

.. note::
  If you just want to kick the tires,
  you might prefer :doc:`datastore-quickstart`.

Creating a project
------------------

.. include:: _components/creating-a-project.rst

Enabling the API
----------------

Now that you created a project,
you need to **turn on** the Cloud Datastore API.
This is sort of like telling Google
which services you intend to use for this project.

* **Click on APIs & Auth**
  on the left hand side,
  and scroll down to where it says
  "Google Cloud Datastore API".

* **Click the "Off" button**
  on the right side
  to turn it into an "On" button.

Enabling a service account
--------------------------

.. include:: _components/enabling-a-service-account.rst

Add some data to your dataset
-----------------------------

Open a Python console and...

  >>> from gcloud import datastore
  >>> datastore.set_defaults()
  >>> list(datastore.Query(kind='Person').fetch())
  []
  >>> entity = datastore.Entity(key=datastore.Key('Person'))
  >>> entity['name'] = 'Your name'
  >>> entity['age'] = 25
  >>> entity.save()
  >>> list(Query(kind='Person').fetch())
  [<Entity{...} {'name': 'Your name', 'age': 25}>]

And that's it!
--------------

Next,
take a look at the complete
:doc:`datastore-api`.
