Google Cloud Python Client
==========================

The goal of this project is to make it really simple and Pythonic
to use Google Cloud Platform services.

Quickstart
----------

The library is ``pip``-installable::

  $ pip install gcloud
  $ python -m gcloud.storage.demo  # Runs the storage demo!

Documentation
-------------

- `gcloud docs (browse all services, quick-starts, walk-throughs) <http://GoogleCloudPlatform.github.io/gcloud-python/>`_
- `gcloud.datastore API docs <http://googlecloudplatform.github.io/gcloud-python/datastore-api.html>`_
- `gcloud.storage API docs <http://googlecloudplatform.github.io/gcloud-python/storage-api.html>`_
- gcloud.bigquery API docs (*coming soon)*
- gcloud.compute API docs *(coming soon)*
- gcloud.dns API docs *(coming soon)*
- gcloud.sql API docs *(coming soon)*

I'm getting weird errors... Can you help?
-----------------------------------------

Chances are you have some dependency problems...
If you're on Ubuntu,
try installing the pre-compiled packages::

  $ sudo apt-get install python-crypto python-openssl libffi-dev

or try installing the development packages
(that have the header files included)
and then ``pip install`` the dependencies again::

  $ sudo apt-get install python-dev libssl-dev libffi-dev
  $ pip install gcloud

How do I build the docs?
------------------------

Make sure you have ``sphinx`` installed and::

  $ git clone git://github.com/GoogleCloudPlatform/gcloud-python.git
  $ pip install sphinx
  $ cd gcloud-python/docs
  $ make html

How do I run the tests?
-----------------------

Make sure you have ``nose`` installed and::

  $ git clone git://github.com/GoogleCloudPlatform/gcloud-python.git
  $ pip install unittest2 nose
  $ cd gcloud-python
  $ nosetests

How can I contribute?
---------------------

Before we can accept any pull requests
we have to jump through a couple of legal hurdles,
primarily a Contributor License Agreement (CLA):

- **If you are an individual writing original source code**
  and you're sure you own the intellectual property,
  then you'll need to sign an `individual CLA
  <http://code.google.com/legal/individual-cla-v1.0.html>`_.
- **If you work for a company that wants to allow you to contribute your work**,
  then you'll need to sign a `corporate CLA
  <http://code.google.com/legal/corporate-cla-v1.0.html>`_.

You can sign these electronically (just scroll to the bottom).
After that, we'll be able to accept your pull requests.
