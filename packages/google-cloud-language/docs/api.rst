Language Client API Reference
=============================

This package includes clients for multiple versions of the Natural Language
API. By default, you will get ``v1``, the latest GA version.

.. toctree::
  :maxdepth: 2

  language_v1/services
  language_v1/types

If you are interested in beta features ahead of the latest GA, you may
opt-in to the v1.1 beta, which is spelled ``v1beta2``. In order to do this,
you will want to import from ``google.cloud.language_v1beta2`` in lieu of
``google.cloud.language``.

An API and type reference is provided for the v1.1 beta also:

.. toctree::
  :maxdepth: 2

  language_v1beta2/services
  language_v1beta2/types

Migration Guide
---------------

See the guide below for instructions on migrating to the 2.x release of this library.

.. toctree::
    :maxdepth: 2

    UPGRADING

.. note::

  The client for the beta API is provided on a provisional basis. The API
  surface is subject to change, and it is possible that this client will be
  deprecated or removed after its features become GA.
