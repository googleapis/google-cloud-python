Contributing
============

#. **Please sign one of the contributor license agreements below.**
#. Fork the repo, develop and test your code changes, add docs.
#. Make sure that your commit messages clearly describe the changes.
#. Send a pull request.

Here are some guidelines for hacking on ``google-auth-library-python``.

Making changes
--------------

A few notes on making changes to ``google-auth-libary-python``.

- If you've added a new feature or modified an existing feature, be sure to
  add or update any applicable documentation in docstrings and in the
  documentation (in ``docs/``). You can re-generate the reference documentation
  using ``tox -e docgen``.

- The change must work fully on the following CPython versions: 2.7,
  3.4, and 3.5 across macOS, Linux, and Windows.

- The codebase *must* have 100% test statement coverage after each commit.
  You can test coverage via ``tox -e cover``.

Testing changes
---------------

To test your changes, run unit tests with ``tox``::

    $ tox -e py27
    $ tox -e py34
    $ tox -e py35

Coding Style
------------

This library is PEP8 & Pylint compliant. Our Pylint config is defined at
``pylintrc`` for package code and ``pylintrc.tests`` for test code. Use
``tox`` to check for non-compliant code::

   $ tox -e lint

Documentation Coverage and Building HTML Documentation
------------------------------------------------------

If you fix a bug, and the bug requires an API or behavior modification, all
documentation in this package which references that API or behavior must be
changed to reflect the bug fix, ideally in the same commit that fixes the bug
or adds the feature.

To build and review docs use  ``tox``::

   $ tox -e docs

The HTML version of the docs will be built in ``docs/_build/html``

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
