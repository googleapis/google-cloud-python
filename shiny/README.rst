Python Client for Google Shiny New API
======================================

    Python idiomatic client for `Google Shiny New API`_

.. _Google Shiny New API: https://cloud.google.com/shiny/docs

-  `Documentation`_

.. _Documentation: https://googlecloudplatform.github.io/google-cloud-python/stable/shiny-usage.html

Quick Start
-----------

.. code-block:: console

    $ pip install --upgrade google-cloud-shiny

Authentication
--------------

With ``google-cloud-python`` we try to make authentication as painless as
possible. Check out the `Authentication section`_ in our documentation to
learn more. You may also find the `authentication document`_ shared by all
the ``google-cloud-*`` libraries to be helpful.

.. _Authentication section: http://google-cloud-python.readthedocs.io/en/latest/google-cloud-auth.html
.. _authentication document: https://github.com/GoogleCloudPlatform/gcloud-common/tree/master/authentication

Using the API
-------------

The Google Shiny New API is a fully pretend, magical unicorn, widget
frobulation system. It allows you to do nothing while actually
doing something.

.. code:: python

    from google.cloud import shiny

    client = shiny.Client()
    # Create a unicorn bound to the current client.
    unicorn = client.unicorn('Boris')
    # Do "nothing" with this unicorn.
    unicorn.do_nothing()
