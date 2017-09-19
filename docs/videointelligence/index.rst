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
  :class:`~google.cloud.videointelligence_v1beta2.VideoIntelligenceServiceClient`.

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

.. warning::
    
    The video intelligence API is currently in beta. While the ``v1beta2`` endpoint
    will continue to work for some time, when the GA version comes out, the client
    library will automatically move to it.
    
    If you wish, you can pin to the beta version explicitly, and it will continue
    to be supported. If so, use the following import statement:
    
    .. code-block:: python
    
        from google.cloud import videointelligence_v1beta2

This package includes clients for multiple versions of the Natural Language
API. By default, you will get ``v1beta2``, the latest beta version. When the GA
version is released, it will become the default (as described in the warning above).

.. toctree::
    :maxdepth: 2

    gapic/v1beta2/api
    gapic/v1beta2/types

The previous beta release, spelled ``v1beta1``, is provided to continue to support
code previously written against it. In order to use this, 
you will want to import from ``google.cloud.videointelligence_v1beta1`` in lieu of
``google.cloud.videointelligence_v1beta1``.

An API and type reference is provided the first beta also:

.. toctree::
    :maxdepth: 2

    gapic/v1beta1/api
    gapic/v1beta1/types
