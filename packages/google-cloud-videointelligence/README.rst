Python Client for Google Cloud Video Intelligence
=================================================

|ga| |pypi| |versions| 

`Google Cloud Video Intelligence`_ API makes videos searchable, and
discoverable, by extracting metadata with an easy to use API.
You can now search every moment of every video file in your catalog
and find every occurrence as well as its significance. It quickly
annotates videos stored in `Google Cloud Storage`_, and helps you
identify key nouns entities of your video, and when they occur
within the video. Separate signal from noise, by retrieving
relevant information at the video, shot or per frame.

- `Client Library Documentation`_
- `Product Documentation`_

.. |ga| image:: https://img.shields.io/badge/support-ga-gold.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/master/README.rst#ga-support
.. |pypi| image:: https://img.shields.io/pypi/v/google-cloud-videointelligence.svg
   :target: https://pypi.org/project/google-cloud-videointelligence/
.. |versions| image:: https://img.shields.io/pypi/pyversions/google-cloud-videointelligence.svg
   :target: https://pypi.org/project/google-cloud-videointelligence/
.. _Google Cloud Video Intelligence: https://cloud.google.com/video-intelligence/
.. _Google Cloud Storage: https://cloud.google.com/storage/
.. _Client Library Documentation: https://googleapis.dev/python/videointelligence/latest
.. _Product Documentation: https://cloud.google.com/video-intelligence/docs/

Quick Start
-----------

In order to use this library, you first need to go through the following steps:

1. `Select or create a Cloud Platform project.`_
2. `Enable billing for your project.`_
3. `Enable the Google Cloud Video Intelligence API.`_
4. `Setup Authentication.`_

.. _Select or create a Cloud Platform project.: https://console.cloud.google.com/project
.. _Enable billing for your project.: https://cloud.google.com/billing/docs/how-to/modify-project#enable_billing_for_a_project
.. _Enable the Google Cloud Video Intelligence API.:  https://cloud.google.com/datastore
.. _Setup Authentication.: https://googleapis.dev/python/google-api-core/latest/auth.html

Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With `virtualenv`_, it's possible to install this library without needing system
install permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/

Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^
Python >= 3.6

Unsupported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Python == 2.7.

The last version of this library compatible with Python 2.7 is google-cloud-videointelligence==1.17.0.

Mac/Linux
^^^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-cloud-videointelligence

Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-cloud-videointelligence

Example Usage
~~~~~~~~~~~~~

.. code-block:: python

   from google.cloud import videointelligence
   
   client = videointelligence.VideoIntelligenceServiceClient()
   job = client.annotate_video(
       input_uri='gs://<bucket-name>/my_video.mp4',
       features=['LABEL_DETECTION', 'SHOT_CHANGE_DETECTION'],
   )
   result = job.result()

Next Steps
~~~~~~~~~~

-  Read the `Client Library Documentation`_ for Google Cloud Video Intelligence 
   API to see other available methods on the client.
-  Read the `Product documentation`_ to learn
   more about the product and see How-to Guides.
