.. toctree::
  :maxdepth: 1
  :hidden:

Authentication
--------------

==============
Quick overview
==============

**If you're running in Compute Engine or App Engine**,
authentication should "just work"
as credentials can be loaded automatically
and therefore there is no extra code required to authenticate.

**If you're developing locally**,
the easiest way to authenticate is using the Cloud SDK.

**If you're running your application elsewhere**,
you should download a service account JSON keyfile
and point to it using an environment variable.

------------------------------------------------------
In what order does gcloud-python discover credentials?
------------------------------------------------------

``gcloud-python`` will look in a bunch of different places
for authentication credentials, in the following order:

#. Credentials you explicitly set in code
#. Credentials provided when running in Google App Engine
#. Credentials from an environment variable (``GOOGLE_APPLICATION_CREDENTIALS``)
#. Credentials provided by the Cloud SDK (``gcloud auth login``)
#. Credentials provided when running in Google Compute Engine

This means that you can set your credentials a bunch of different ways.
We recommend using some form of implicitly discovered credentials
(ie, set in an environment variable or auto-discovered in GCE/GAE)
so that your code can be
run in the environment of your choice
with no changes.

=========================================
Authenticating locally with the Cloud SDK
=========================================

This is the easiest way to authenticate while you're developing locally.

#. Download and install the Cloud SDK (You can get the Cloud SDK at https://cloud.google.com/sdk)
#. Authenticate using OAuth2 (``gcloud auth login``)
#. Run your code (ie, ``python myscript.py``)


After you do this,
your script will look for the authentication token
that you got when authenticating,
and you won't need to think about authentication in your code at all.

.. note::

  Remember, this is **not** a recommended authentication method
  for running your code in production.
  Use the Cloud SDK only while developing locally.

======================================
Authenticating with a specific keyfile
======================================

----------------------------------------------
Setting the keyfile in an environment variable
----------------------------------------------

If you have a specific JSON keyfile downloaded that you'd like to use,
you can simply set the path to this in
the ``GOOGLE_APPLICATION_CREDENTIALS`` environment variable.

This means your code doesn't have to change at all,
and can run with different credentials depending on the environment.

Here's what this looks like:

.. code-block:: bash

   $ export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
   $ python
   >>> from gcloud import pubsub
   >>> pubsub.Topic('topic_name').create()

--------------------------------------
Setting the keyfile explicitly in code
--------------------------------------

If you really want to set a specific keyfile in code
(maybe for a code snippet to send to a friend?)
you can do this, but it's really not recommended.

~~~~~~~~~~~~~~~~~~~~~~~~
... using a JSON keyfile
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from gcloud.credentials import get_for_service_account_json
   from gcloud import pubsub

   # Create the credentials from the keyfile and set the default connection.
   credentials = get_for_service_account_json('/path/to/key.json')
   connection = pubsub.Connection(credentials=credentials)
   pubsub.set_default_connection(connection)

   # Now you can interact with the service as usual.
   pubsub.Topic('topic_name').create()

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
... using a .p12 key and client email
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from gcloud.credentials import get_for_service_account_p12
   from gcloud import pubsub

   # Create the credentials from the .p12 file and set the default connection.
   credentials = get_for_service_account_p12(
       'special-email-for-p12@developer.gserviceaccount.com',
       '/path/to/key.p12')
   connection = pubsub.Connection(credentials=credentials)
   pubsub.set_default_connection(connection)

   # Now you can interact with the service as usual.
   pubsub.Topic('topic_name').create()

=====================================
Authenticating from inside GCE or GAE
=====================================

If you're application is inside
Google Compute Engine or Google App Engine,
no extra work is needed.
You should simply write your code as though you've already authenticated
as we can discover your credentials and Project ID automatically.

The following code should "just work" inside GAE or GCE:

.. code-block:: python

   from gcloud import pubsub
   pubsub.Topic('topic_name').create()

---------------------------------------
Using a different key inside GCE or GAE
---------------------------------------

You might be running inside GCE or GAE but want to
use a different Service Account.
In that case, jump up to the section about
using a specific keyfile.
Thanks to the order of evaluation,
the keyfile you specify explicitly or via the environment variable
will take precedence over the automatically discovered key in the
App Engine or Compute Engine environment.

===========================================
Using multiple credentials in the same code
===========================================

There may be times where you want to use
multiple different sets of credentials inside the same script.
To do this, you should create multiple connections
and specify which to use on the various API calls you make.

For example, here is how you would create two Pub/Sub topics
in two different projects
with two different sets of credentials.

.. code-block:: python

   from gcloud import pubsub
   from gcloud.credentials import get_for_service_account_json

   # Create two different credentials.
   credentials1 = get_for_service_account_json('key1.json')
   credentials2 = get_for_service_account_json('key2.json')

   # Create two different connections.
   connection1 = pubsub.Connection(credentials=credentials1)
   connection2 = pubsub.Connection(credentials=credentials2)

   # Create two different topics.
   pubsub.Topic('topic1', project='project1', connection=connection1).create()
   pubsub.Topic('topic2', project='project2', connection=connection2).create()

If you have one "main" set of credentials
and others are "one-offs" for special cases,
you can avoid all this typing
by using the default connection for the main set,
and separate connections for the others.

Using the same example as before,
and assuming ``'key1.json'`` is the "main" set of credentials,
here's what that same code might look like.

.. code-block:: python

   from gcloud import pubsub
   from gcloud.credentials import get_for_service_account_json

   credentials2 = get_for_service_account_json('key2.json')
   connection2 = pubsub.Connection(credentials=credentials2)

   pubsub.Topic('topic1').create()
   pubsub.Topic('topic2', project='project2', connection=connection2).create()

===============
Troubleshooting
===============

--------------------------------------------------
You keep mentioning key.json... How do I get that?
--------------------------------------------------

When we say ``key.json``
we're referring to the set of credentials for a "Service Account".
A service account is like a user account for a machine
(rather than a human) and
the `key.json` file allows the account to authenticate.

Service Accounts are pretty easy to create,
just head over to the `Credentials`_ page
in the `Google Developers Console`_,
create a new Client ID,
and generate a new JSON key.

If you're a bit confused,
take a look at the step by step guide here:
https://cloud.google.com/storage/docs/authentication#service_accounts

----------------------------------------------------------------
I'm running in Compute Engine, but can't access Datastore. Help?
----------------------------------------------------------------

When you create your Compute Engine instance,
you need to specify which services this particular instance has access to
(you might not want all of your machines to access Datastore for example).

To do this,
click on "Show advanced options" on the "New Instance" page
(at the top of the screen, towards the right),
scroll down to the section called "Project Access",
and set the appropriate access
for the service you want your VM to have
(ie, Datastore -> Enabled).

.. note::

   Unfortunately,
   you can't change these settings after the VM is created.
   Hopefully Google will change this in the future.

-------------------------------
I'm still having trouble. Help?
-------------------------------

If you're having trouble authenticating,
feel free to open a `Github Issue`_ on this project
and hopefully we can help
(and add the answer to your question here).

.. _Google Developers Console: https://console.developers.google.com/project
.. _Credentials: https://console.developers.google.com/project/_/apiui/credential
.. _Github Issue: https://github.com/GoogleCloudPlatform/gcloud-python/issues/new?title=Authentication+question
