Contributing
============================

#. **Please sign one of the contributor license agreements below.**
#. Fork the repo, develop and test your code changes, add docs.
#. Make sure that your commit messages clearly describe the changes.
#. Send a pull request.

Here are some guidelines for hacking on ``gcloud-python``.

Using a Development Checkout
----------------------------

You'll have to create a development environment to hack on ``gcloud-python``,
using a Git checkout:

- While logged into your GitHub account, navigate to the ``gcloud-python`` repo
  on GitHub.

  https://github.com/GoogleCloudPlatform/gcloud-python

- Fork and clone the ``gcloud-python`` repository to your GitHub account by
  clicking the "Fork" button.

- Clone your fork of ``gcloud-python`` from your GitHub account to your local
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

- Create a virtualenv in which to install ``gcloud-python``::

   $ cd ~/hack-on-gcloud
   $ virtualenv --python python2.7 env

  Note that very old versions of virtualenv (virtualenv versions below, say,
  1.10 or thereabouts) require you to pass a ``--no-site-packages`` flag to
  get a completely isolated environment.

  You can choose which Python version you want to use by passing a ``--python``
  flag to ``virtualenv``.  For example, ``virtualenv --python python2.7``
  chooses the Python 2.7 interpreter to be installed.

  From here on in within these instructions, the ``~/hack-on-gcloud/env``
  virtual environment you created above will be referred to as ``$VENV``.
  To use the instructions in the steps that follow literally, use the
  ``export VENV=~/hack-on-gcloud/env`` command.

- Install ``gcloud-python`` from the checkout into the virtualenv using
  ``setup.py develop``.  Running ``setup.py develop`` *must* be done while
  the current working directory is the ``gcloud-python`` checkout directory::

   $ cd ~/hack-on-gcloud
   $ $VENV/bin/python setup.py develop

I'm getting weird errors... Can you help?
-----------------------------------------

If the error mentions ``Python.h`` not being found,
install ``python-dev`` and try again.
On Debian/Ubuntu::

  $ sudo apt-get install python-dev

Adding Features
---------------

In order to add a feature to ``gcloud-python``:

- The feature must be documented in both the API and narrative
  documentation (in ``docs/``).

- The feature must work fully on the following CPython versions:  2.7,
  3.4, and 3.5 on both UNIX and Windows.

- The feature must not add unnecessary dependencies (where
  "unnecessary" is of course subjective, but new dependencies should
  be discussed).

Coding Style
------------

- PEP8 compliance, with exceptions defined in ``tox.ini``.
  If you have ``tox`` installed, you can test that you have not introduced
  any non-compliant code via::

   $ tox -e lint

- In order to make ``tox -e lint`` run faster, you can set some environment
  variables::

   export GCLOUD_REMOTE_FOR_LINT="upstream"
   export GCLOUD_BRANCH_FOR_LINT="master"

  By doing this, you are specifying the location of the most up-to-date
  version of ``gcloud-python``. The the suggested remote name ``upstream``
  should point to the official ``GoogleCloudPlatform`` checkout and the
  the branch should be the main branch on that remote (``master``).

Exceptions to PEP8:

- Many unit tests use a helper method, ``_callFUT`` ("FUT" is short for
  "Function-Under-Test"), which is PEP8-incompliant, but more readable.
  Some also use a local variable, ``MUT`` (short for "Module-Under-Test").

Running Tests
--------------

- To run all tests for ``gcloud-python`` on a single Python version, run
  ``py.test`` from your development virtualenv (See
  *Using a Development Checkout* above).

- To run the full set of ``gcloud-python`` tests on all platforms, install
  ``tox`` (https://testrun.org/tox/) into a system Python.  The ``tox`` console
  script will be installed into the scripts location for that Python.  While
  ``cd``'ed to the ``gcloud-python`` checkout root directory (it contains
  ``tox.ini``), invoke the ``tox`` console script.  This will read the
  ``tox.ini`` file and execute the tests on multiple Python versions and
  platforms; while it runs, it creates a virtualenv for each version/platform
  combination.  For example::

   $ sudo /usr/bin/pip install tox
   $ cd ~/hack-on-gcloud/
   $ /usr/bin/tox

Running System Tests
--------------------

- To run system tests you can execute::

   $ tox -e system-tests

  or run only system tests for a particular package via::

   $ python system_tests/run_system_test.py --package {package}

  This alone will not run the tests. You'll need to change some local
  auth settings and change some configuration in your project to
  run all the tests.

- System tests will be run against an actual project and
  so you'll need to provide some environment variables to facilitate
  authentication to your project:

  - ``GCLOUD_TESTS_PROJECT_ID``: Developers Console project ID (e.g.
    bamboo-shift-455).
  - ``GOOGLE_APPLICATION_CREDENTIALS``: The path to a JSON key file;
    see ``system_tests/app_credentials.json.sample`` as an example. Such a file
    can be downloaded directly from the developer's console by clicking
    "Generate new JSON key". See private key
    `docs <https://cloud.google.com/storage/docs/authentication#generating-a-private-key>`__
    for more details. In order for Logging system tests to work, the Service Account
    will also have to be made a project Owner. This can be changed under "IAM & Admin".

- Examples of these can be found in ``system_tests/local_test_setup.sample``. We
  recommend copying this to ``system_tests/local_test_setup``, editing the
  values and sourcing them into your environment::

   $ source system_tests/local_test_setup

- For datastore tests, you'll need to create composite
  `indexes <https://cloud.google.com/datastore/docs/tools/indexconfig>`__
  with the ``gcloud`` command line
  `tool <https://developers.google.com/cloud/sdk/gcloud/>`__::

   # Install the app (App Engine Command Line Interface) component.
   $ gcloud components update app

   # See https://cloud.google.com/sdk/crypto for details on PyOpenSSL and
   # http://stackoverflow.com/a/25067729/1068170 for why we must persist.
   $ export CLOUDSDK_PYTHON_SITEPACKAGES=1

   # Authenticate the gcloud tool with your account.
   $ JSON_CREDENTIALS_FILE="path/to/app_credentials.json"
   $ gcloud auth activate-service-account --key-file=$JSON_CREDENTIALS_FILE

   # Create the indexes
   $ gcloud preview datastore create-indexes system_tests/data/index.yaml \
   > --project=$GCLOUD_TESTS_PROJECT_ID

   # Restore your environment to its previous state.
   $ unset CLOUDSDK_PYTHON_SITEPACKAGES

- For datastore query tests, you'll need stored data in your dataset.
  To populate this data, run::

   $ python system_tests/populate_datastore.py

- If you make a mistake during development (i.e. a failing test that
  prevents clean-up) you can clear all system test data from your
  datastore instance via::

   $ python system_tests/clear_datastore.py

- System tests can also be run against local `emulators`_ that mock
  the production services. To run the system tests with the
  ``datastore`` emulator::

   $ tox -e datastore-emulator

  This also requires that the ``gcloud`` command line tool is
  installed. If you'd like to run them directly (outside of a
  ``tox`` environment), first start the emulator and
  take note of the process ID::

   $ gcloud beta emulators datastore start 2>&1 > log.txt &
   [1] 33333

  then determine the environment variables needed to interact with
  the emulator::

   $ gcloud beta emulators datastore env-init
   export DATASTORE_LOCAL_HOST=localhost:8417
   export DATASTORE_HOST=http://localhost:8417
   export DATASTORE_DATASET=gcloud-settings-app-id
   export DATASTORE_PROJECT_ID=gcloud-settings-app-id

  using these environment variables run the emulator::

   $ DATASTORE_HOST=http://localhost:8471 \
   >   DATASTORE_DATASET=gcloud-settings-app-id \
   >   GCLOUD_NO_PRINT=true \
   >   python system_tests/run_system_test.py \
   >   --package=datastore --ignore-requirements

  and after completion stop the emulator and any child
  processes it spawned::

   $ kill -- -33333

.. _emulators: https://cloud.google.com/sdk/gcloud/reference/beta/emulators/

- To run the system tests with the ``pubsub`` emulator::

   $ tox -e pubsub-emulator

  If you'd like to run them directly (outside of a ``tox`` environment), first
  start the emulator and take note of the process ID::

   $ gcloud beta emulators pubsub start 2>&1 > log.txt &
   [1] 44444

  then determine the environment variables needed to interact with
  the emulator::

   $ gcloud beta emulators pubsub env-init
   export PUBSUB_EMULATOR_HOST=localhost:8897

  using these environment variables run the emulator::

   $ PUBSUB_EMULATOR_HOST=localhost:8897 \
   >   python system_tests/run_system_test.py \
   >   --package=pubsub

  and after completion stop the emulator and any child
  processes it spawned::

   $ kill -- -44444

Test Coverage
-------------

- The codebase *must* have 100% test statement coverage after each commit.
  You can test coverage via ``tox -e cover``.

Documentation Coverage and Building HTML Documentation
------------------------------------------------------

If you fix a bug, and the bug requires an API or behavior modification, all
documentation in this package which references that API or behavior must be
changed to reflect the bug fix, ideally in the same commit that fixes the bug
or adds the feature.

To build and review docs (where ``$VENV`` refers to the virtualenv you're
using to develop ``gcloud-python``):

1. After following the steps above in "Using a Development Checkout", install
   Sphinx and all development requirements in your virtualenv::

     $ cd ~/hack-on-gcloud
     $ $VENV/bin/pip install Sphinx

2. Change into the ``docs`` directory within your ``gcloud-python`` checkout and
   execute the ``make`` command with some flags::

     $ cd ~/hack-on-gcloud/gcloud-python/docs
     $ make clean html SPHINXBUILD=$VENV/bin/sphinx-build

   The ``SPHINXBUILD=...`` argument tells Sphinx to use the virtualenv Python,
   which will have both Sphinx and ``gcloud-python`` (for API documentation
   generation) installed.

3. Open the ``docs/_build/html/index.html`` file to see the resulting HTML
   rendering.

As an alternative to 1. and 2. above, if you have ``tox`` installed, you
can build the docs via::

   $ tox -e docs

In addition, to build a preview of the `readthedocs`_ theme, you can
build via::

   $ tox -e docs-rtd

.. _readthedocs: http://gcloud-python.readthedocs.org/

Note About ``README`` as it pertains to PyPI
--------------------------------------------

The `description on PyPI`_ for the project comes directly from the
``README``. Due to the reStructuredText (``rst``) parser used by
PyPI, relative links which will work on GitHub (e.g. ``CONTRIBUTING.rst``
instead of
``https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/CONTRIBUTING.rst``)
may cause problems creating links or rendering the description.

.. _description on PyPI: https://pypi.python.org/pypi/gcloud

Travis Configuration and Build Optimizations
--------------------------------------------

All build scripts in the ``.travis.yml`` configuration file which have
Python dependencies are specified in the ``tox.ini`` configuration.
They are executed in the Travis build via ``tox -e {ENV}`` where
``{ENV}`` is the environment being tested.

If new ``tox`` environments are added to be run in a Travis build, they
should be listed in ``[tox].envlist`` as a default environment.

We speed up builds by using the Travis `caching feature`_.

.. _caching feature: https://docs.travis-ci.com/user/caching/#pip-cache

We intentionally **do not** cache the ``.tox/`` directory. Instead, we
allow the ``tox`` environments to be re-built for every build. This
way, we'll always get the latest versions of our dependencies and any
caching or wheel optimization to be done will be handled automatically
by ``pip``.

Supported Python Versions
-------------------------

We support:

-  `Python 2.7`_
-  `Python 3.4`_
-  `Python 3.5`_

.. _Python 2.7: https://docs.python.org/2.7/
.. _Python 3.4: https://docs.python.org/3.4/
.. _Python 3.5: https://docs.python.org/3.5/

Supported versions can be found in our ``tox.ini`` `config`_.

.. _config: https://github.com/GoogleCloudPlatform/gcloud-python/blob/master/tox.ini

We explicitly decided not to support `Python 2.5`_ due to `decreased usage`_
and lack of continuous integration `support`_.

.. _Python 2.5: https://docs.python.org/2.5/
.. _decreased usage: https://caremad.io/2013/10/a-look-at-pypi-downloads/
.. _support: http://blog.travis-ci.com/2013-11-18-upcoming-build-environment-updates/

We have `dropped 2.6`_ as a supported version as well since Python 2.6 is no
longer supported by the core development team.

We also explicitly decided to support Python 3 beginning with version
3.4. Reasons for this include:

-  Encouraging use of newest versions of Python 3
-  Taking the lead of `prominent`_ open-source `projects`_
-  `Unicode literal support`_ which allows for a cleaner codebase that
   works in both Python 2 and Python 3

.. _prominent: https://docs.djangoproject.com/en/1.9/faq/install/#what-python-version-can-i-use-with-django
.. _projects: http://flask.pocoo.org/docs/0.10/python3/
.. _Unicode literal support: https://www.python.org/dev/peps/pep-0414/
.. _dropped 2.6: https://github.com/GoogleCloudPlatform/gcloud-python/issues/995

Versioning
----------

This library follows `Semantic Versioning`_.

.. _Semantic Versioning: http://semver.org/

It is currently in major version zero (``0.y.z``), which means that anything
may change at any time and the public API should not be considered
stable.

Contributor License Agreements
------------------------------

Before we can accept your pull requests you'll need to sign a Contributor License Agreement (CLA):

- **If you are an individual writing original source code** and **you own the intellectual property**, then you'll need to sign an `individual CLA <https://developers.google.com/open-source/cla/individual>`__.
- **If you work for a company that wants to allow you to contribute your work**, then you'll need to sign a `corporate CLA <https://developers.google.com/open-source/cla/corporate>`__.

You can sign these electronically (just scroll to the bottom). After that, we'll be able to accept your pull requests.
