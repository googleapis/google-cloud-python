:maxdepth: 1

.. toctree::
  :hidden:

  datastore-api
  storage-api
  common-api

Google Cloud Python API
=======================

.. warning::
  This library is **still under construction**
  and is **not** the official Google Python API client library.

Getting started
---------------

If you've never used ``gcloud`` before,
you should probably take a look at
:doc:`getting-started`.

Services
--------

.. topic:: Cloud Datastore
  :class: service

  .. image:: /_static/datastore-logo.png
    :target: datastore-api.html

  - Google's `official documentation <https://developers.google.com/datastore/>`_
  - :doc:`datastore-quickstart`
  - :doc:`datastore-getting-started`
  - :doc:`Cloud Datastore API Documentation <datastore-api>`

.. topic:: Cloud Storage
  :class: service

  .. image:: /_static/storage-logo.png
    :target: storage-api.html

  - Google's `official documentation <https://developers.google.com/storage/>`_
  - :doc:`storage-quickstart`
  - `Getting started with Cloud Storage <https://github.com/GoogleCloudPlatform/gcloud-python/issues/37>`_
  - :doc:`Cloud Storage API Documentation <storage-api>`

.. topic:: Compute Engine
  :class: service

  .. image:: /_static/compute-logo.png
    :target: https://github.com/GoogleCloudPlatform/gcloud-python/issues/34

  - Google's `official documentation <https://developers.google.com/compute/>`_
  - Coming soon...

.. topic:: Cloud SQL
  :class: service

  .. image:: /_static/cloudsql-logo.png
    :target: https://github.com/GoogleCloudPlatform/gcloud-python/issues/35

  - Google's `official documentation <https://developers.google.com/cloud-sql/>`_
  - Coming soon...

.. topic:: Big Query
  :class: service

  .. image:: /_static/bigquery-logo.png
    :target: https://github.com/GoogleCloudPlatform/gcloud-python/issues/36

  - Google's `official documentation <https://developers.google.com/bigquery/>`_
  - Coming soon...

Common modules
--------------

- :doc:`Common Module API Documentation <common-api>`

How to contribute
-----------------

Want to help out?
That's awesome.
The library is open source
and `lives on GitHub <https://github.com/GoogleCloudPlatform/gcloud-python>`_.
Open an issue
or fork the library and submit a pull request.

Keep in mind that before we can accept any pull requests
we have to jump through a couple of legal hurdles,
primarily a Contributor License Agreement (CLA):

- **If you are an individual writing original source code**
  and you're sure you own the intellectual property,
  then you'll need to sign an `individual CLA
  <http://code.google.com/legal/individual-cla-v1.0.html>`_.
- **If you work for a company that wants to allow you to contribute your work**,
  then you'll need to sign a `corporate CLA
  <http://code.google.com/legal/corporate-cla-v1.0.html>`_.

Follow either of the two links above to access the appropriate CLA
and instructions for how to sign and return it.
Once we receive it, we'll be able to accept your pull requests.
