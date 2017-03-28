####################
Using the Vision API
####################


********************************
Authentication and Configuration
********************************

- For an overview of authentication in ``google-cloud-python``,
  see :doc:`google-cloud-auth`.

- In addition to any authentication configuration, you should also set the
  :envvar:`GOOGLE_CLOUD_PROJECT` environment variable for the project you'd
  like to interact with. If the GOOGLE_CLOUD_PROJECT environment variable is
  not present, the project ID from JSON file credentials is used.

  If you are using Google App Engine or Google Compute Engine
  this will be detected automatically.

- After configuring your environment, create a
  :class:`~google.cloud.vision.client.Client`.

.. code-block:: python

     >>> from google.cloud import vision
     >>> client = vision.Client()

or pass in ``credentials`` and ``project`` explicitly.

.. code-block:: python

     >>> from google.cloud import vision
     >>> client = vision.Client(project='my-project', credentials=creds)


*****************************************************
Creating an :class:`~google.cloud.vision.image.Image`
*****************************************************

The :class:`~google.cloud.vision.image.Image` class is used to load image
data from sources such as a Google Cloud Storage URI, raw bytes, or a file.


From a Google Cloud Storage URI
===============================

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> image = client.image(source_uri='gs://my-test-bucket/image.jpg')


From a filename
===============

.. code-block:: python

    >>> image = client.image(filename='image.jpg')

From raw bytes
==============

.. code-block:: python

    >>> with open('./image.jpg', 'rb') as image_file:
    ...     bytes_image = client.image(content=image_file.read())


****************
Manual Detection
****************

You can call the detection method manually.

.. code-block:: python

    >>> from google.cloud import vision
    >>> from google.cloud.vision.feature import Feature
    >>> from google.cloud.vision.feature import FeatureTypes
    >>> client = vision.Client()
    >>> image = client.image(source_uri='gs://my-test-bucket/image.jpg')
    >>> features = [Feature(FeatureTypes.FACE_DETECTION, 5),
    ...             Feature(FeatureTypes.LOGO_DETECTION, 3)]
    >>> annotations = image.detect(features)
    >>> len(annotations.faces)
    2
    >>> for face in annotations.faces:
    ...     print(face.joy_likelihood)
    0.94099093
    0.54453093
    >>> len(annotations.logos)
    2
    >>> for logo in annotations.logos:
    ...     print(logo.description)
    'google'
    'github'


**********
Crop Hints
**********

:meth:`~google.cloud.vision.image.Image.detect_crop_hints` will attempt to find
boundaries that contain interesting data which can be used to crop an image.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> image = client.image(source_uri='gs://my-test-bucket/image.jpg')
    >>> crop_hints = image.detect_crop_hints(aspect_ratios=[1.3333], limit=2)
    >>> first_hint = crop_hints[0]
    >>> first_hint.bounds.vertices[0].x_coordinate
    77
    >>> first_hint.bounds.vertices[0].y_coordinate
    102
    >>> first_hint.confidence
    0.5
    >>> first_hint.importance_fraction
    1.22000002861


**************
Face Detection
**************

:meth:`~google.cloud.vision.image.Image.detect_faces` will search for faces in
an image and return the coordinates in the image of each `landmark type`_ that
was detected.

.. _landmark type: https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#type_1

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> image = client.image(source_uri='gs://my-test-bucket/image.jpg')
    >>> faces = image.detect_faces(limit=10)
    >>> first_face = faces[0]
    >>> first_face.landmarks.left_eye.landmark_type
    <LandmarkTypes.LEFT_EYE: 'LEFT_EYE'>
    >>> first_face.landmarks.left_eye.position.x_coordinate
    1301.2404
    >>> first_face.detection_confidence
    0.9863683
    >>> first_face.joy
    <Likelihood.VERY_LIKELY: 'VERY_LIKELY'>
    >>> first_face.anger
    <Likelihood.VERY_UNLIKELY: 'VERY_UNLIKELY'>


***************
Label Detection
***************

:meth:`~google.cloud.vision.image.Image.detect_labels` will attempt to label
objects in an image. If there is a car, person and a dog in the image, label
detection will attempt to identify those objects and score the level of
certainty from ``0.0 to 1.0``.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> image = client.image(source_uri='gs://my-storage-bucket/image.jpg')
    >>> labels = image.detect_labels(limit=3)
    >>> labels[0].description
    'automobile'
    >>> labels[0].score
    0.9863683


******************
Landmark Detection
******************

:meth:`~google.cloud.vision.image.Image.detect_landmarks` will attempt to
detect landmarks such as "Mount Rushmore" and the "Sydney Opera House". The API
will also provide their known geographical locations if available.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     image = client.image(content=image_file.read())
    >>> landmarks = image.detect_landmarks()
    >>> landmarks[0].description
    'Sydney Opera House'
    >>> landmarks[0].locations[0].latitude
    -33.857123
    >>> landmarks[0].locations[0].longitude
    151.213921
    >>> landmarks[0].bounds.vertices[0].x_coordinate
    78
    >>> landmarks[0].bounds.vertices[0].y_coordinate
    162


**************
Logo Detection
**************

With :meth:`~google.cloud.vision.image.Image.detect_logos`, you can identify
brand logos in an image. Their shape and location in the image can be found by
iterating through the detected logo's ``vertices``.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     image = client.image(content=image_file.read())
    >>> logos = image.detect_logos(limit=3)
    >>> print(len(logos))
    3
    >>> first_logo = logos[0]
    >>> first_logo.description
    'Google'
    >>> first_logo.score
    0.9795432
    >>> print(len(first_logo.bounds.vertices))
    4
    >>> first_logo.bounds.vertices[0].x_coordinate
    78
    >>> first_logo.bounds.vertices[0].y_coordinate
    62


*********************
Safe Search Detection
*********************

:meth:`~google.cloud.vision.image.Image.detect_safe_search` will try to
categorize the entire contents of the image under four categories.

- adult: Represents the likelihood that the image contains adult content.
- spoof: The likelihood that an obvious modification was made to the image's
  canonical version to make it appear funny or offensive.
- medical: Likelihood this is a medical image.
- violence: Violence likelihood.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     image = client.image(content=image_file.read())
    >>> safe_search = image.detect_safe_search()
    >>> safe_search.adult
    <Likelihood.VERY_UNLIKELY: 'VERY_UNLIKELY'>
    >>> safe_search.spoof
    <Likelihood.POSSIBLE: 'POSSIBLE'>
    >>> safe_search.medical
    <Likelihood.VERY_LIKELY: 'VERY_LIKELY'>
    >>> safe_search.violence
    <Likelihood.LIKELY: 'LIKELY'>


**************
Text Detection
**************

:meth:`~google.cloud.vision.image.Image.detect_text` performs OCR to find text
in an image.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     image = client.image(content=image_file.read())
    >>> texts = image.detect_text()
    >>> texts[0].locale
    'en'
    >>> texts[0].description
    'some text in the image'
    >>> texts[1].description
    'some other text in the image'


****************
Image Properties
****************

:meth:`~google.cloud.vision.image.Image.detect_properties` will process the
image and determine the dominant colors in the image.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     image = client.image(content=image_file.read())
    >>> properties = image.detect_properties()
    >>> colors = properties.colors
    >>> first_color = colors[0]
    >>> first_color.red
    244.0
    >>> first_color.blue
    134.0
    >>> first_color.score
    0.65519291
    >>> first_color.pixel_fraction
    0.758658


*********************
Batch image detection
*********************

Multiple images can be processed with a single request by passing
:class:`~google.cloud.vision.image.Image` to
:meth:`~google.cloud.vision.client.Client.batch()`.

.. code-block:: python

    >>> from google.cloud import vision
    >>> from google.cloud.vision.feature import Feature
    >>> from google.cloud.vision.feature import FeatureTypes
    >>>
    >>> client = vision.Client()
    >>> batch = client.batch()
    >>>
    >>> image_one = client.image(source_uri='gs://my-test-bucket/image1.jpg')
    >>> image_two = client.image(source_uri='gs://my-test-bucket/image2.jpg')
    >>> face_feature = Feature(FeatureTypes.FACE_DETECTION, 2)
    >>> logo_feature = Feature(FeatureTypes.LOGO_DETECTION, 2)
    >>> batch.add_image(image_one, [face_feature, logo_feature])
    >>> batch.add_image(image_two, [logo_feature])
    >>> results = batch.detect()
    >>> for image in results:
    ...     for face in image.faces:
    ...         print('=' * 40)
    ...         print(face.joy)
    ========================================
    <Likelihood.VERY_LIKELY: 'VERY_LIKELY'>
    ========================================
    <Likelihood.VERY_LIKELY: 'POSSIBLE'>


*************
Web Detection
*************

:meth:`~google.cloud.vision.image.Image.detect_web` search for images on the
web that are similar to the image you have.

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     image = client.image(content=image_file.read())
    >>> web_images = image.detect_web(limit=2)
    >>> for full_matching_image in web_images.full_matching_images:
    ...     print('=' * 20)
    ...     print(full_matching_image.url)
    ====================
    'https://example.com/image.jpg'
    >>> for partial_matching_image in web_images.partial_matching_images:
    ...     print('=' * 20)
    ...     print(partial_matching_image.url)
    ====================
    >>> for page_with_matching_images in web_images.pages_with_matching_images:
    ...     print('=' * 20)
    ...     print(page_with_matching_images.url)
    ====================
    'https://example.com/portfolio/'
    >>> for entity in web_images.web_entities:
    ...     print('=' * 20)
    ...     print(entity.description)
    ====================
    'Mount Rushmore National Memorial'
    ====================
    'Landmark'


****************
No results found
****************

If no results for the detection performed can be extracted from the image, then
an empty list is returned. This behavior is similiar with all detection types.


Example with :meth:`~google.cloud.vision.image.Image.detect_logos`:

.. code-block:: python

    >>> from google.cloud import vision
    >>> client = vision.Client()
    >>> with open('./image.jpg', 'rb') as image_file:
    ...     image = client.image(content=image_file.read())
    >>> logos = image.detect_logos(limit=3)
    >>> logos
    []
