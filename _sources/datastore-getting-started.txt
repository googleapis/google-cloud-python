Getting started with Cloud Datastore
====================================

.. note::
  If you just want to kick the tires,
  you might prefer :doc:`datastore-quickstart`.

Creating a project
------------------

* **Create a project**

  Start off by visiting https://cloud.google.com/console
  and click on the big red button
  that says "Create Project".

* **Choose a name**

  In the box that says "name",
  choose something friendly.
  This is going to be the *human-readable* name
  for your project.

* **Choose an ID**

  In the box that says "ID",
  choose something unique
  (hyphens are OK).
  I typically choose a project name
  that starts with my initials,
  then a hyphen,
  then a unique identifier for the work I'm doing.
  For this example,
  you might choose ``<initials>-quickstart``.

Then click OK
(give it a second to create your project).

Enable the Cloud Datastore API
------------------------------

Now that you created a project,
you need to *turn on* the Cloud Datastore API.
This is sort of like telling Google
which services you intend to use for this project.

* **Click on APIs & Auth**
  on the left hand side,
  and scroll down to where it says
  "Google Cloud Datastore API".

* **Click the "Off" button**
  on the right side
  to turn it into an "On" button.

Enable a "Service Account"
--------------------------

Now that you have a project
that has access to the Cloud Datastore API,
we need to make sure we are able to access our data.
There are many ways to authenticate,
but we're going to use a Service Account for today.

A *Service Account* is sort of like a username and password
(like when you're connecting to your MySQL database),
except the username is automatically generated
(and is an e-mail address)
and the password is actually a private key file.

To create a Service Account:

* **Click on Credentials**
  under the "APIs & Auth" section.

* **Click the big red button**
  that says "Create New Client ID"
  under the OAuth section
  (the first one).

* **Choose "Service Account"**
  and click the blue button
  that says "Create Client ID".

* **This will automatically**
  download a private key file.
  **Do not lost this.**

* **Rename your key** something shorter.
  I like to name the key ``<project name>.key``.

  This is like your password for the account.

* **Copy the long weird e-mail address**
  labeled "E-mail address"
  in the information section
  for the Service Account
  you just created.

  This is like your username for the account.

OK. That's it!
Time to start doing things with your Cloud Datastore project.

Add some data to your dataset
-----------------------------

Open a Python console and...

  >>> from gcloud import datastore
  >>> dataset = datastore.get_dataset(
  >>>     '<your-project-id-here',
  >>>     '<the e-mail address you copied here>',
  >>>     '/path/to/<your project>.key')
  >>> dataset.query().fetch()
  []
  >>> entity = dataset.entity('Person')
  >>> entity['name'] = 'Your name'
  >>> entity['age'] = 25
  >>> entity.save()
  >>> dataset.query('Person').fetch()
  [<Entity{...} {'name': 'Your name', 'age': 25}>]

And that's it!
--------------

Next,
take a look at the complete
:doc:`datastore-api`.
