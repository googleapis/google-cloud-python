############
Contributing
############

#. **Please sign one of the contributor license agreements below.**
#. Fork the repo, develop and test your code changes, add docs.
#. Make sure that your commit messages clearly describe the changes.
#. Send a pull request. (Please Read: `Faster Pull Request Reviews`_)

.. _Faster Pull Request Reviews: https://github.com/kubernetes/community/blob/master/contributors/guide/pull-requests.md#best-practices-for-faster-reviews

.. contents:: Here are some guidelines for hacking on ``google-cloud-python``.

***************
Adding Features
***************

In order to add a feature to ``google-cloud-python``:

- The feature must be documented in both the API and narrative
  documentation (in ``docs/``).

- The feature must work fully on the following CPython versions:  2.7,
  3.5, 3.6, and 3.7 on both UNIX and Windows.

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

To work on the codebase and run the tests, we recommend using ``nox``,
but you can also use a ``virtualenv`` of your own creation.

.. _repo: https://github.com/GoogleCloudPlatform/google-cloud-python

Using ``nox``
=============

We use `nox <https://nox.readthedocs.io/en/latest/>`__ to instrument our tests.

- To test your changes, run unit tests with ``nox``::

    $ nox -f datastore/noxfile.py -s unit-2.7
    $ nox -f datastore/noxfile.py -s unit-3.7
    $ ...

  .. note::

    The unit tests and system tests are contained in the individual
    ``nox.py`` files in each directory; substitute ``datastore`` in the
    example above with the package of your choice.


  Alternatively, you can just navigate directly to the package you are
  currently developing and run tests there::

    $ export GIT_ROOT=$(pwd)
    $ cd ${GIT_ROOT}/datastore/
    $ nox -s "unit(py='3.7')"

.. nox: https://pypi.org/project/nox-automation/

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

- PEP8 compliance, with exceptions defined in the linter configuration.
  If you have ``nox`` installed, you can test that you have not introduced
  any non-compliant code via::

   $ nox -s lint

- In order to make ``nox -s lint`` run faster, you can set some environment
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

********************
Running System Tests
********************

- To run system tests for a given package, you can execute::

   $ nox -f datastore/noxfile.py -s system-3.7
   $ nox -f datastore/noxfile.py -s system-2.7

  .. note::

      System tests are only configured to run under Python 2.7 and
      Python 3.7. For expediency, we do not run them in older versions
      of Python 3.

  This alone will not run the tests. You'll need to change some local
  auth settings and change some configuration in your project to
  run all the tests.

- System tests will be run against an actual project and
  so you'll need to provide some environment variables to facilitate
  authentication to your project:

  - ``GOOGLE_APPLICATION_CREDENTIALS``: The path to a JSON key file;
    Such a file can be downloaded directly from the developer's console by clicking
    "Generate new JSON key". See private key
    `docs <https://cloud.google.com/storage/docs/authentication#generating-a-private-key>`__
    for more details.

  - In order for Logging system tests to work, the Service Account
    will also have to be made a project ``Owner``. This can be changed under
    "IAM & Admin". Additionally, ``cloud-logs@google.com`` must be given
    ``Editor`` permissions on the project.

- Once you have downloaded your json keys, set the environment variable 
  ``GOOGLE_APPLICATION_CREDENTIALS`` to the absolute path of the json file::

   $ export GOOGLE_APPLICATION_CREDENTIALS="/Users/<your_username>/path/to/app_credentials.json"

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
   $ gcloud datastore indexes create datastore/tests/system/index.yaml

- For datastore query tests, you'll need stored data in your dataset.
  To populate this data, run::

   $ python datastore/tests/system/utils/populate_datastore.py

- If you make a mistake during development (i.e. a failing test that
  prevents clean-up) you can clear all system test data from your
  datastore instance via::

   $ python datastore/tests/system/utils/clear_datastore.py


******************************
Running Generated Sample Tests
******************************

- To run system tests for a given package, you can execute::

   $ nox -f speech/noxfile.py -s samples

  .. note::

      Generated sample tests require the ``sample-tester`` commamd line
      `tool <https://sample-tester.readthedocs.io>`.

- Generated sample tests will be run against an actual project and
  so you'll need to provide some environment variables to facilitate
  authentication to your project (See: Running System Tests)


*************
Test Coverage
*************

- The codebase *must* have 100% test statement coverage after each commit.
  You can test coverage via ``nox -s cover``.

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

As an alternative to 1. and 2. above, if you have ``nox`` installed, you
can build the docs via::

   $ nox -s docs

********************************************
Note About ``README`` as it pertains to PyPI
********************************************

The `description on PyPI`_ for the project comes directly from the
``README``. Due to the reStructuredText (``rst``) parser used by
PyPI, relative links which will work on GitHub (e.g. ``CONTRIBUTING.rst``
instead of
``https://github.com/GoogleCloudPlatform/google-cloud-python/blob/master/CONTRIBUTING.rst``)
may cause problems creating links or rendering the description.

.. _description on PyPI: https://pypi.org/project/google-cloud/

**********************
CircleCI Configuration
**********************

All build scripts in the ``.circleci/config.yml`` configuration file which have
Python dependencies are specified in the ``nox.py`` configuration.
They are executed in the Travis build via ``nox -s ${ENV}`` where
``${ENV}`` is the environment being tested.


*************************
Supported Python Versions
*************************

We support:

-  `Python 3.5`_
-  `Python 3.6`_
-  `Python 3.7`_

.. _Python 3.5: https://docs.python.org/3.5/
.. _Python 3.6: https://docs.python.org/3.6/
.. _Python 3.7: https://docs.python.org/3.7/


Supported versions can be found in our ``noxfile.py`` `config`_.

.. _config: https://github.com/googleapis/google-cloud-python/blob/master/noxfile.py

We explicitly decided not to support `Python 2.5`_ due to `decreased usage`_
and lack of continuous integration `support`_.

.. _Python 2.5: https://docs.python.org/2.5/
.. _decreased usage: https://caremad.io/2013/10/a-look-at-pypi-downloads/
.. _support: https://blog.travis-ci.com/2013-11-18-upcoming-build-environment-updates/

We have `dropped 2.6`_ as a supported version as well since Python 2.6 is no
longer supported by the core development team.

Python 2.7 support is deprecated. All code changes should maintain Python 2.7 compatibility until January 1, 2020.

We also explicitly decided to support Python 3 beginning with version
3.5. Reasons for this include:

-  Encouraging use of newest versions of Python 3
-  Taking the lead of `prominent`_ open-source `projects`_
-  `Unicode literal support`_ which allows for a cleaner codebase that
   works in both Python 2 and Python 3

.. _prominent: https://docs.djangoproject.com/en/1.9/faq/install/#what-python-version-can-i-use-with-django
.. _projects: http://flask.pocoo.org/docs/0.10/python3/
.. _Unicode literal support: https://www.python.org/dev/peps/pep-0414/
.. _dropped 2.6: https://github.com/googleapis/google-cloud-python/issues/995

**********
Versioning
**********

This library follows `Semantic Versioning`_.

.. _Semantic Versioning: http://semver.org/

Some packages are currently in major version zero (``0.y.z``), which means that
anything may change at any time and the public API should not be considered
stable.

******************************
Contributor License Agreements
******************************

Before we can accept your pull requests you'll need to sign a Contributor
License Agreement (CLA):

- **If you are an individual writing original source code** and **you own the
  intellectual property**, then you'll need to sign an
  `individual CLA <https://developers.google.com/open-source/cla/individual>`__.
- **If you work for a company that wants to allow you to contribute your work**,
  then you'll need to sign a
  `corporate CLA <https://developers.google.com/open-source/cla/corporate>`__.

You can sign these electronically (just scroll to the bottom). After that,
we'll be able to accept your pull requests.
