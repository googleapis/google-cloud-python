############
Contributing
############

#. **Please sign one of the contributor license agreements below.**
#. Fork the repo, develop and test your code changes, add docs.
#. Make sure that your commit messages clearly describe the changes.
#. Send a pull request. (Please Read: `Faster Pull Request Reviews`_)

.. _Faster Pull Request Reviews: https://github.com/kubernetes/community/blob/master/contributors/devel/faster_reviews.md

.. contents:: Here are some guidelines for hacking on ``google-cloud-python``.

***************
Adding Features
***************

In order to add a feature to ``google-cloud-python``:

- The feature must be documented in both the API and narrative
  documentation (in ``docs/``).

- The feature must work fully on the following CPython versions:  2.7,
  3.4, and 3.5 on both UNIX and Windows.

- The feature must not add unnecessary dependencies (where
  "unnecessary" is of course subjective, but new dependencies should
  be discussed).

****************************
Using a Development Checkout
****************************

You'll have to create a development environment to hack on
``google-cloud-python``, using a Git checkout:

- While logged into your GitHub account, navigate to the
  ``google-cloud-python`` `repo`_ on GitHub.

- Fork and clone the ``google-cloud-python`` repository to your GitHub account by
  clicking the "Fork" button.

- Clone your fork of ``google-cloud-python`` from your GitHub account to your local
  computer, substituting your account username and specifying the destination
  as ``hack-on-google-cloud-python``.  E.g.::

   $ cd ${HOME}
   $ git clone git@github.com:USERNAME/google-cloud-python.git hack-on-google-cloud-python
   $ cd hack-on-google-cloud-python
   # Configure remotes such that you can pull changes from the google-cloud-python
   # repository into your local repository.
   $ git remote add upstream git@github.com:GoogleCloudPlatform/google-cloud-python.git
   # fetch and merge changes from upstream into master
   $ git fetch upstream
   $ git merge upstream/master

Now your local repo is set up such that you will push changes to your GitHub
repo, from which you can submit a pull request.

To work on the codebase and run the tests, we recommend using ``tox``,
but you can also use a ``virtualenv`` of your own creation.

.. _repo: https://github.com/GoogleCloudPlatform/google-cloud-python

Using a custom ``virtualenv``
=============================

- To create a virtualenv in which to install ``google-cloud-python``::

    $ cd ${HOME}/hack-on-google-cloud-python
    $ virtualenv --python python2.7 ${ENV_NAME}

  You can choose which Python version you want to use by passing a ``--python``
  flag to ``virtualenv``.  For example, ``virtualenv --python python2.7``
  chooses the Python 2.7 interpreter to be installed.

- From here on in within these instructions, the
  ``${HOME}/hack-on-google-cloud-python/${ENV_NAME}`` virtual environment you
  created above will be referred to as ``${VENV}``. To use the instructions
  in the steps that follow literally, use::

    $ export VENV=${HOME}/hack-on-google-cloud-python/${ENV_NAME}

- To install ``google-cloud-python`` from your source checkout into
  ``${VENV}``, run::

    $ # Make sure you are in the same directory as setup.py
    $ cd ${HOME}/hack-on-google-cloud-python
    $ ${VENV}/bin/python setup.py install

  Unfortunately using ``setup.py develop`` is not possible with this
  project, because it uses `namespace packages`_.

Using ``tox``
=============

- To test your changes, run unit tests with ``tox``::

    $ tox -e py27
    $ tox -e py34
    $ ...

- If you'd like to poke around your code in an interpreter, let
  ``tox`` install the environment of your choice::

    $ # Install only; without running tests
    $ tox -e ${ENV} --recreate --notest

  After doing this, you can activate the virtual environment and
  use the interpreter from that environment::

    $ source .tox/${ENV}/bin/activate
    (ENV) $ .tox/${ENV}/bin/python

  Unfortunately, your changes to the source tree won't be picked up
  by the ``tox`` environment, so if you make changes, you'll need
  to again ``--recreate`` the environment.

- To run unit tests on a restricted set of packages::

    $ tox -e py27 -- core datastore

  Alternatively, you can just navigate directly to the package you are
  currently developing and run tests there::

    $ export GIT_ROOT=$(pwd)
    $ cd ${GIT_ROOT}/core/
    $ tox -e py27
    $ cd ${GIT_ROOT}/datastore/
    $ tox -e py27

Note on Editable Installs / Develop Mode
========================================

- As mentioned previously, using ``setuptools`` in `develop mode`_
  or a ``pip`` `editable install`_ is not possible with this
  library. This is because this library uses `namespace packages`_.
  For context see `Issue #2316`_ and the relevant `PyPA issue`_.

  Since ``editable`` / ``develop`` mode can't be used, packages
  need to be installed directly. Hence your changes to the source
  tree don't get incorporated into the **already installed**
  package.

.. _namespace packages: https://www.python.org/dev/peps/pep-0420/
.. _Issue #2316: https://github.com/GoogleCloudPlatform/google-cloud-python/issues/2316
.. _PyPA issue: https://github.com/pypa/packaging-problems/issues/12
.. _develop mode: https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode
.. _editable install: https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs

*****************************************
I'm getting weird errors... Can you help?
*****************************************

If the error mentions ``Python.h`` not being found,
install ``python-dev`` and try again.
On Debian/Ubuntu::

  $ sudo apt-get install python-dev

************
Coding Style
************

- PEP8 compliance, with exceptions defined in ``tox.ini``.
  If you have ``tox`` installed, you can test that you have not introduced
  any non-compliant code via::

   $ tox -e lint

- In order to make ``tox -e lint`` run faster, you can set some environment
  variables::

   export GOOGLE_CLOUD_TESTING_REMOTE="upstream"
   export GOOGLE_CLOUD_TESTING_BRANCH="master"

  By doing this, you are specifying the location of the most up-to-date
  version of ``google-cloud-python``. The the suggested remote name ``upstream``
  should point to the official ``GoogleCloudPlatform`` checkout and the
  the branch should be the main branch on that remote (``master``).

Exceptions to PEP8:

- Many unit tests use a helper method, ``_call_fut`` ("FUT" is short for
  "Function-Under-Test"), which is PEP8-incompliant, but more readable.
  Some also use a local variable, ``MUT`` (short for "Module-Under-Test").

*************
Running Tests
*************

- To run all tests for ``google-cloud-python`` on a single Python version, run
  ``py.test`` from your development virtualenv (See
  `Using a Development Checkout`_ above).

.. _Using a Development Checkout: #using-a-development-checkout

- To run the full set of ``google-cloud-python`` tests on all platforms, install
  ``tox`` (https://tox.readthedocs.io/en/latest/) into a system Python.  The
  ``tox`` console script will be installed into the scripts location for that
  Python.  While ``cd``'-ed to the ``google-cloud-python`` checkout root
  directory (it contains ``tox.ini``), invoke the ``tox`` console script.
  This will read the ``tox.ini`` file and execute the tests on multiple
  Python versions and platforms; while it runs, it creates a ``virtualenv`` for
  each version/platform combination.  For example::

   $ sudo --set-home /usr/bin/pip install tox
   $ cd ${HOME}/hack-on-google-cloud-python/
   $ /usr/bin/tox

.. _Using a Development Checkout: #using-a-development-checkout

********************
Running System Tests
********************

- To run system tests you can execute::

   $ tox -e system-tests
   $ tox -e system-tests3

  or run only system tests for a particular package via::

   $ python system_tests/run_system_test.py --package {package}
   $ python3 system_tests/run_system_test.py --package {package}

  To run a subset of the system tests::

   $ tox -e system-tests -- datastore storage
   $ python system_tests/attempt_system_tests.py datastore storage

  This alone will not run the tests. You'll need to change some local
  auth settings and change some configuration in your project to
  run all the tests.

- System tests will be run against an actual project and
  so you'll need to provide some environment variables to facilitate
  authentication to your project:

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
   $ gcloud components install app-engine-python

   # Authenticate the gcloud tool with your account.
   $ GOOGLE_APPLICATION_CREDENTIALS="path/to/app_credentials.json"
   $ gcloud auth activate-service-account \
   > --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

   # Create the indexes
   $ gcloud datastore create-indexes system_tests/data/index.yaml

- For datastore query tests, you'll need stored data in your dataset.
  To populate this data, run::

   $ python system_tests/populate_datastore.py

- If you make a mistake during development (i.e. a failing test that
  prevents clean-up) you can clear all system test data from your
  datastore instance via::

   $ python system_tests/clear_datastore.py

System Test Emulators
=====================

- System tests can also be run against local `emulators`_ that mock
  the production services. To run the system tests with the
  ``datastore`` emulator::

   $ tox -e datastore-emulator
   $ GOOGLE_CLOUD_DISABLE_GRPC=true tox -e datastore-emulator

  This also requires that the ``gcloud`` command line tool is
  installed. If you'd like to run them directly (outside of a
  ``tox`` environment), first start the emulator and
  take note of the process ID::

   $ gcloud beta emulators datastore start --no-legacy 2>&1 > log.txt &
   [1] 33333

  then determine the environment variables needed to interact with
  the emulator::

   $ gcloud beta emulators datastore env-init
   export DATASTORE_LOCAL_HOST=localhost:8417
   export DATASTORE_HOST=http://localhost:8417
   export DATASTORE_DATASET=google-cloud-settings-app-id
   export DATASTORE_PROJECT_ID=google-cloud-settings-app-id

  using these environment variables run the emulator::

   $ DATASTORE_HOST=http://localhost:8471 \
   >   DATASTORE_DATASET=google-cloud-settings-app-id \
   >   GOOGLE_CLOUD_NO_PRINT=true \
   >   python system_tests/run_system_test.py \
   >   --package=datastore --ignore-requirements

  and after completion stop the emulator and any child
  processes it spawned::

   $ kill -- -33333

.. _emulators: https://cloud.google.com/sdk/gcloud/reference/beta/emulators/

- To run the system tests with the ``pubsub`` emulator::

   $ tox -e pubsub-emulator
   $ GOOGLE_CLOUD_DISABLE_GRPC=true tox -e pubsub-emulator

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

*************
Test Coverage
*************

- The codebase *must* have 100% test statement coverage after each commit.
  You can test coverage via ``tox -e cover``.

******************************************************
Documentation Coverage and Building HTML Documentation
******************************************************

If you fix a bug, and the bug requires an API or behavior modification, all
documentation in this package which references that API or behavior must be
changed to reflect the bug fix, ideally in the same commit that fixes the bug
or adds the feature.

To build and review docs (where ``${VENV}`` refers to the virtualenv you're
using to develop ``google-cloud-python``):

#. After following the steps above in "Using a Development Checkout", install
   Sphinx and all development requirements in your virtualenv::

     $ cd ${HOME}/hack-on-google-cloud-python
     $ ${VENV}/bin/pip install Sphinx

#. Change into the ``docs`` directory within your ``google-cloud-python`` checkout and
   execute the ``make`` command with some flags::

     $ cd ${HOME}/hack-on-google-cloud-python/google-cloud-python/docs
     $ make clean html SPHINXBUILD=${VENV}/bin/sphinx-build

   The ``SPHINXBUILD=...`` argument tells Sphinx to use the virtualenv Python,
   which will have both Sphinx and ``google-cloud-python`` (for API documentation
   generation) installed.

#. Open the ``docs/_build/html/index.html`` file to see the resulting HTML
   rendering.

As an alternative to 1. and 2. above, if you have ``tox`` installed, you
can build the docs via::

   $ tox -e docs

********************************************
Note About ``README`` as it pertains to PyPI
********************************************

The `description on PyPI`_ for the project comes directly from the
``README``. Due to the reStructuredText (``rst``) parser used by
PyPI, relative links which will work on GitHub (e.g. ``CONTRIBUTING.rst``
instead of
``https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/CONTRIBUTING.rst``)
may cause problems creating links or rendering the description.

.. _description on PyPI: https://pypi.python.org/pypi/google-cloud

********************************************
Travis Configuration and Build Optimizations
********************************************

All build scripts in the ``.travis.yml`` configuration file which have
Python dependencies are specified in the ``tox.ini`` configuration.
They are executed in the Travis build via ``tox -e ${ENV}`` where
``${ENV}`` is the environment being tested.

If new ``tox`` environments are added to be run in a Travis build, they
should be listed in ``[tox].envlist`` as a default environment.

We speed up builds by using the Travis `caching feature`_.

.. _caching feature: https://docs.travis-ci.com/user/caching/#pip-cache

We intentionally **do not** cache the ``.tox/`` directory. Instead, we
allow the ``tox`` environments to be re-built for every build. This
way, we'll always get the latest versions of our dependencies and any
caching or wheel optimization to be done will be handled automatically
by ``pip``.

*************************
Supported Python Versions
*************************

We support:

-  `Python 2.7`_
-  `Python 3.4`_
-  `Python 3.5`_

.. _Python 2.7: https://docs.python.org/2.7/
.. _Python 3.4: https://docs.python.org/3.4/
.. _Python 3.5: https://docs.python.org/3.5/

Supported versions can be found in our ``tox.ini`` `config`_.

.. _config: https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/tox.ini

We explicitly decided not to support `Python 2.5`_ due to `decreased usage`_
and lack of continuous integration `support`_.

.. _Python 2.5: https://docs.python.org/2.5/
.. _decreased usage: https://caremad.io/2013/10/a-look-at-pypi-downloads/
.. _support: https://blog.travis-ci.com/2013-11-18-upcoming-build-environment-updates/

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
.. _dropped 2.6: https://github.com/GoogleCloudPlatform/google-cloud-python/issues/995

**********
Versioning
**********

This library follows `Semantic Versioning`_.

.. _Semantic Versioning: http://semver.org/

It is currently in major version zero (``0.y.z``), which means that anything
may change at any time and the public API should not be considered
stable.

******************************
Contributor License Agreements
******************************

Before we can accept your pull requests you'll need to sign a Contributor License Agreement (CLA):

- **If you are an individual writing original source code** and **you own the intellectual property**, then you'll need to sign an `individual CLA <https://developers.google.com/open-source/cla/individual>`__.
- **If you work for a company that wants to allow you to contribute your work**, then you'll need to sign a `corporate CLA <https://developers.google.com/open-source/cla/corporate>`__.

You can sign these electronically (just scroll to the bottom). After that, we'll be able to accept your pull requests.
