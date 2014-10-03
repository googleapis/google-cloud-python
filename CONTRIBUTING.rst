Hacking on ``gcloud-python``
============================

Here are some guidelines for hacking on gcloud-python.

Using a Development Checkout
----------------------------

You'll have to create a development environment to hack on gcloud-python,
using a Git checkout:

- While logged into your GitHub account, navigate to the gcloud-python repo on
  GitHub.
  
  https://github.com/GoogleCloudPlatform/gcloud-python

- Fork and clone the gcloud-python repository to your GitHub account by
  clicking the "Fork" button.

- Clone your fork of gcloud-python from your GitHub account to your local
  computer, substituting your account username and specifying the destination
  as "hack-on-gcloud".  E.g.::

   $ cd ~
   $ git clone git@github.com:USERNAME/gcloud-python.git hack-on-gcloud
   $ cd hack-on-gcloud
   # Configure remotes such that you can pull changes from the gcloud-python
   # repository into your local repository.
   $ git remote add upstream https://github.com:GoogleCloudPlatform/gcloud-python
   # fetch and merge changes from upstream into master
   $ git fetch upstream
   $ git merge upstream/master

Now your local repo is set up such that you will push changes to your GitHub
repo, from which you can submit a pull request.

- Create a virtualenv in which to install gcloud-python::

   $ cd ~/hack-on-gcloud
   $ virtualenv -ppython2.7 env

  Note that very old versions of virtualenv (virtualenv versions below, say,
  1.10 or thereabouts) require you to pass a ``--no-site-packages`` flag to
  get a completely isolated environment.

  You can choose which Python version you want to use by passing a ``-p``
  flag to ``virtualenv``.  For example, ``virtualenv -ppython2.7``
  chooses the Python 2.7 interpreter to be installed.

  From here on in within these instructions, the ``~/hack-on-gcloud/env``
  virtual environment you created above will be referred to as ``$VENV``.
  To use the instructions in the steps that follow literally, use the
  ``export VENV=~/hack-on-gcloud/env`` command.

- Install gcloud-python from the checkout into the virtualenv using
  ``setup.py develop``.  Running ``setup.py develop`` *must* be done while
  the current working directory is the ``gcloud-python`` checkout directory::

   $ cd ~/hack-on-gcloud
   $ $VENV/bin/python setup.py develop

Adding Features
---------------

In order to add a feature to gcloud-python:

- The feature must be documented in both the API and narrative
  documentation (in ``docs/``).

- The feature must work fully on the following CPython versions: 2.6,
  and 2.7 on both UNIX and Windows.

- The feature must not add unnecessary dependencies (where
  "unnecessary" is of course subjective, but new dependencies should
  be discussed).

Coding Style
------------

- PEP8 compliance, with exceptions defined in ``tox.ini``.
  If you have ``tox`` installed, you can test that you have not introduced
  any non-compliant code via::

   $ tox -e lint

Exceptions to PEP8:

- Many unit tests use a helper method, ``_callFUT`` ("FUT" is short for
  "Function-Under-Test"), which is PEP8-incompliant, but more readable.
  Some also use a local variable, ``MUT`` (short for "Module-Under-Test").

Running Tests
--------------

- To run all tests for gcloud-python on a single Python version, run
  ``nosetests`` from your development virtualenv (See
  *Using a Development Checkout* above).

- To run the full set of gcloud-python tests on all platforms, install ``tox``
  (http://codespeak.net/~hpk/tox/) into a system Python.  The ``tox`` console
  script will be installed into the scripts location for that Python.  While
  ``cd``'ed to the gcloud-python checkout root directory (it contains ``tox.ini``),
  invoke the ``tox`` console script.  This will read the ``tox.ini`` file and
  execute the tests on multiple Python versions and platforms; while it runs,
  it creates a virtualenv for each version/platform combination.  For
  example::

   $ sudo /usr/bin/pip install tox
   $ cd ~/hack-on-gcloud/
   $ /usr/bin/tox


Test Coverage
-------------

- The codebase *must* have 100% test statement coverage after each commit.
  You can test coverage via ``tox -e coverage``, or alternately by installing
  ``nose`` and ``coverage`` into your virtualenv, and running
  ``setup.py nosetests --with-coverage``.  If you have ``tox`` installed::

   $ tox -e cover

Documentation Coverage and Building HTML Documentation
------------------------------------------------------

If you fix a bug, and the bug requires an API or behavior modification, all
documentation in this package which references that API or behavior must be
changed to reflect the bug fix, ideally in the same commit that fixes the bug
or adds the feature.

To build and review docs (where ``$VENV`` refers to the virtualenv you're
using to develop gcloud-python):

1. After following the steps above in "Using a Development Checkout", install
   Sphinx and all development requirements in your virtualenv::

     $ cd ~/hack-on-gcloud
     $ $VENV/bin/pip install Sphinx

2. Change into the ``docs`` directory within your gcloud-python checkout and
   execute the ``make`` command with some flags::

     $ cd ~/hack-on-gcloud/gcloud-python/docs
     $ make clean html SPHINXBUILD=$VENV/bin/sphinx-build

   The ``SPHINXBUILD=...`` argument tells Sphinx to use the virtualenv Python,
   which will have both Sphinx and gcloud-python (for API documentation
   generation) installed.

3. Open the ``docs/_build/html/index.html`` file to see the resulting HTML
   rendering.

As an alternative to 1. and 2. above, if you have ``tox`` installed, you
can build the docs via::

   $ tox -e docs

Change Log
----------

- Feature additions and bugfixes must be added to the ``CHANGES.txt``
  file in the prevailing style.  Changelog entries should be long and
  descriptive, not cryptic.  Other developers should be able to know
  what your changelog entry means.
