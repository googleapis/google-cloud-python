Google Cloud
============

Official documentation
----------------------

If you just want to **use** the library
(not contribute to it),
check out the official documentation:
http://GoogleCloudPlatform.github.io/gcloud-python/

Incredibly quick demo
---------------------

Start by cloning the repository::

  $ git clone git://github.com/GoogleCloudPlatform/gcloud-python.git
  $ cd gcloud
  $ python setup.py develop

I'm getting weird errors... Can you help?
-----------------------------------------

Chances are you have some dependency problems,
if you're on Ubuntu,
try installing the pre-compiled packages::

  $ sudo apt-get install python-crypto python-openssl

or try installing the development packages
(that have the header files included)
and then ``pip install`` the dependencies again::

  $ sudo apt-get install python-dev libssl-dev

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
  $ nosetests
