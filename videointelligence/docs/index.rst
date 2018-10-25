.. include:: /../videointelligence/README.rst

API Reference
-------------


This package includes clients for multiple versions of the Video Intelligence
API. By default, you will get ``v1``, the latest stable version.

.. toctree::
    :maxdepth: 2

    gapic/v1/api
    gapic/v1/types

A new beta release with additional features over the current stable version,
spelled ``v1p2beta1``, is provided to allow you to use these new features.
These are expected to move into the stable release soon; until then, the
usual beta admonishment (changes are possible, etc.) applies.

An API and type reference is provided for this beta:

.. toctree::
    :maxdepth: 2

    gapic/v1p2beta1/api
    gapic/v1p2beta1/types

The previous beta releases, spelled ``v1p1beta1``, ``v1beta1``, and
``v1beta2``, are provided to continue to support code previously written
against them. In order to use ththem, you will want to import from e.g.
``google.cloud.videointelligence_v1beta2`` in lieu of
``google.cloud.videointelligence_v1``.

An API and type reference is provided the these betas also:

.. toctree::
    :maxdepth: 2

    gapic/v1p1beta1/api
    gapic/v1p1beta1/types
    gapic/v1beta1/api
    gapic/v1beta1/types
    gapic/v1beta2/api
    gapic/v1beta2/types


Changelog
---------

For a list of all ``google-cloud-videointelligence`` releases:

.. toctree::
  :maxdepth: 2

  changelog
