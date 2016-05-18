Using the Vision API
====================

Authentication and Configuration
--------------------------------

- For an overview of authentication in ``gcloud-python``,
  see :doc:`gcloud-auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GCLOUD_PROJECT` environment variable for the project you'd like
  to interact with. If you are Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`Client <gcloud.vision.client.Client>`

  .. doctest::

     >>> from gcloud import vision
     >>> client = vision.Client()

  or pass in ``credentials`` and ``project`` explicitly

  .. doctest::

     >>> from gcloud import vision
     >>> client = vision.Client(project='my-project', credentials=creds)

Annotating an Image
-------------------

Annotate a single image
~~~~~~~~~~~~~~~~~~~~~~~

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/car.jpg', 'r') as f:
    ...     client.annotate(f.read(), vision.FeatureTypes.LABEL_DETECTION, 3)

Annotate multiple images
~~~~~~~~~~~~~~~~~~~~~~~~

.. doctest::

     >>> images = (
     ...     ('./image.jpg', [
     ...         vision.FeatureTypes.LABEL_DETECTION,
     ...         vision.FeatureTypes.LANDMARK_DETECTION]),
     ...     ('./image2.jpg', [
     ...         vision.FeatureTypes.FACE_DETECTION,
     ...         vision.FeatureTypes.TEXT_DETECTION]),)
     >>> annotated_images = []
     >>> for image, feature_types in images:
     ...     annotated_images.append(
     ...         vision_client.annotate(
     ...            image,
     ...            feature_types))

Failing annotations return no results for the feature type requested.

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/car.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                               vision.FeatureTypes.LOGO_DETECTION, 3)
    >>> len(results.logos) # 0

Face Detection
~~~~~~~~~~~~~~

Annotating using the ``FACE_DETECTION`` feature type.


.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/car.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                              vision.FeatureTypes.FACE_DETECTION, 3)
    >>> results.faces[0].landmarks[0].type # LEFT_EYE
    >>> results.faces[0].landmarks[0].position.x # 1301.2404
    >>> results.faces[0].detection_confidence # 0.9863683
    >>> results.faces[0].joy_likelihood # 0.54453093


Label Detection
~~~~~~~~~~~~~~~

Annotating using the ``LABEL_DETECTION`` feature type.

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/car.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                              vision.FeatureTypes.LABEL_DETECTION, 3)
    >>> results.labels[0].description # automobile
    >>> results.labels[0].score # 0.9794637
    >>> results.labels[1].description # vehicle
    >>> results.labels[1].score # 0.9494648
    >>> results.labels[2].description # sports car
    >>> results.labels[2].score # 0.8258028

Landmark Detection
~~~~~~~~~~~~~~~~~~

Annotating using the ``LANDMARK_DETECTION`` feature type.

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/landmark.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                              vision.FeatureTypes.LANDMARK_DETECTION, 3)
    >>> results.landmarks[0].description # Sydney Opera House
    >>> results.landmarks[0].locations[0].latitude # -33.857123
    >>> results.landmarks[0].locations[0].longitude # 151.213921
    >>> results.landmarks[0].bounding_poly.vertices[0].x = 78
    >>> results.landmarks[0].bounding_poly.vertices[0].y = 162

Logo Detection
~~~~~~~~~~~~~~

Annotating using the ``LOGO_DETECTION`` feature type.

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/logo.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                              vision.FeatureTypes.LOGO_DETECTION, 3)
    >>> results.logos[0].description # Google
    >>> results.logos[0].score # 0.9795432
    >>> results.logos[0].bounding_poly.vertices[0].x = 78
    >>> results.logos[0].bounding_poly.vertices[0].y = 162

Safe Search Detection
~~~~~~~~~~~~~~~~~~~~~

Annotating using the ``SAFE_SEARCH_DETECTION`` feature type.

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/logo.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                              vision.FeatureTypes.SAFE_SEARCH_DETECTION)
    >>> results[0].safe.adult # VERY_UNLIKELY
    >>> results[0].safe.medical # UNLIKELY

Text Detection
~~~~~~~~~~~~~~

Annotating using the ``TEXT_DETECTION`` feature type.

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/logo.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                              vision.FeatureTypes.TEXT_DETECTION)
    >>> results[0].locale # en
    >>> results[0].description # the full text of the image.

Image Properties
~~~~~~~~~~~~~~~~

Annotating using the ``IMAGE_PROPERTIES`` feature type.

.. doctest::

    >>> from gcloud import vision
    >>> client = vision.Client(project="my-project-name")
    >>> with open('/tmp/logo.jpg', 'r') as f:
    ...     results = client.annotate(f.read(),
    ...                              vision.FeatureTypes.IMAGE_PROPERTIES)
    >>> results[0].dominant_colors.colors[0].color.red # 244
    >>> results[0].dominant_colors.colors[0].score # 0.65519291
    >>> results[0].dominant_colors.colors[0].pixel_fraction # 0.758658
