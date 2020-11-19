.. include:: README.rst

.. include:: multiprocessing.rst

API Reference
-------------


This package includes clients for multiple versions of the Video Intelligence
API. By default, you will get ``v1``, the latest stable version.

.. toctree::
    :maxdepth: 2

    videointelligence_v1/services
    videointelligence_v1/types

A beta release with additional features over the current stable version,
spelled ``v1p3beta1``, is also provided.
These are expected to move into the stable release; until then, the
usual beta admonishment (changes are possible, etc.) applies.

An API and type reference is provided for this beta:

.. toctree::
    :maxdepth: 2

    videointelligence_v1p3beta1/services
    videointelligence_v1p3beta1/types

The previous beta releases, spelled ``v1p2beta1``, ``v1p1beta1``, and
``v1beta2``, are provided to continue to support code previously written
against them. In order to use ththem, you will want to import from e.g.
``google.cloud.videointelligence_v1beta2`` in lieu of
``google.cloud.videointelligence_v1``.

An API and type reference is provided for these betas also:

.. toctree::
    :maxdepth: 2

    videointelligence_v1p2beta1/services
    videointelligence_v1p2beta1/types
    videointelligence_v1p1beta1/services
    videointelligence_v1p1beta1/types
    videointelligence_v1beta2/services
    videointelligence_v1beta2/types


Migration Guide
---------------

See the guide below for instructions on migrating to the 2.x release of this library.

.. toctree::
    :maxdepth: 2

    UPGRADING


Changelog
---------

For a list of all ``google-cloud-videointelligence`` releases:

.. toctree::
  :maxdepth: 2

  changelog
