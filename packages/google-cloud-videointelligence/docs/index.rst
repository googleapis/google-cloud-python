Video Intelligence
==================

`Google Cloud Video Intelligence`_ API makes videos searchable, and
discoverable, by extracting metadata with an easy to use API.
You can now search every moment of every video file in your catalog
and find every occurrence as well as its significance. It quickly
annotates videos stored in `Google Cloud Storage`_, and helps you
identify key nouns entities of your video, and when they occur
within the video. Separate signal from noise, by retrieving
relevant information at the video, shot or per frame.

.. _Google Cloud Video Intelligence: https://cloud.google.com/video-intelligence/
.. _Google Cloud Storage: https://cloud.google.com/storage/

************
Installation
************

Install the ``google-cloud-videointelligence`` library using ``pip``:

.. code-block:: console

    $ pip install google-cloud-videointelligence


********************************
Authentication and Configuration
********************************

- For an overview of authentication in ``google-cloud-python``,
  see :doc:`/core/auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd
  like to interact with. If the :envvar:`GOOGLE_CLOUD_PROJECT` environment
  variable is not present, the project ID from JSON file credentials is used.

  If you are using Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`~google.cloud.videointelligence_v1.VideoIntelligenceServiceClient`.

.. code-block:: python

     >>> from google.cloud import videointelligence
     >>> client = videointelligence.VideoIntelligenceServiceClient()

or pass in ``credentials`` explicitly.

.. code-block:: python

     >>> from google.cloud import videointelligence
     >>> client = videointelligence.VideoIntelligenceServiceClient(
     ...     credentials=creds,
     ... )


******************
Annotating a Video
******************

To annotate a video, just determine which annotation features you want, and point
the API at your video:

.. code-block:: python

    >>> from google.cloud import videointelligence
    >>>
    >>> client = videointelligence.VideoIntelligenceServiceClient()
    >>> result = client.annotate_video(
    ...     input_uri='gs://cloudmleap/video/next/animals.mp4',
    ...     features=['LABEL_DETECTION', 'SHOT_CHANGE_DETECTION'],
    ... ).result()
    >>> result.annotationResults[0].labelAnnotations[0].description
    'Android'
    >>> result.annotationResults[0].labelAnnotations[1].description
    'Animation'


*************
API Reference
*************


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

For a list of all ``google-cloud-videointelligence`` releases:

.. toctree::
  :maxdepth: 2

  changelog
