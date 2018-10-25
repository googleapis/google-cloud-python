.. include:: /../tasks/README.rst

API Reference
-------------

This package includes clients for multiple versions of the Tasks
API. By default, you will get ``v2beta3``, the latest version.

.. toctree::
    :maxdepth: 2

    gapic/v2beta3/api
    gapic/v2beta3/types

The previous beta release, spelled ``v2beta2``, is provided to continue to
support code previously written against them. In order to use ththem, you
will want to import from e.g.  ``google.cloud.tasks_v2beta2`` in lieu of
``google.cloud.tasks`` (or the equivalent ``google.cloud.tasks_v2beta3``).

An API and type reference is provided the this beta also:

.. toctree::
    :maxdepth: 2

    gapic/v2beta2/api
    gapic/v2beta2/types
