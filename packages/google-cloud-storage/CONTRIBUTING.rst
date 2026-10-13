############
Contributing
############

This package is part of the ``google-cloud-python`` monorepo.

Please refer to the centralized `Contributing Guide`_ at the repository root for general guidelines on how to contribute, set up your development environment, and submit pull requests.

.. _Contributing Guide: https://github.com/googleapis/google-cloud-python/blob/main/CONTRIBUTING.rst

Package-specific test sessions are defined in this directory's ``noxfile.py``. Dependencies and supported Python versions are defined in ``pyproject.toml``.

Run ``nox -s package`` to build and validate the source distribution and wheel.
The ``lint_setup_py`` session remains available for shared repository CI.
Coverage settings are defined in ``pyproject.toml``; unit-test sessions use the
per-Python constraints files in ``testing/``.

Run ``nox -s lint`` to check code or ``nox -s format`` to apply safe fixes and
format it. Ruff settings in ``pyproject.toml`` enable ``E``, ``F``, ``W``, ``I``,
and ``UP`` for Python 3.10 and newer.
