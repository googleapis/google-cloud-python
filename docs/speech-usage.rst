Using the API
=============

The `Google Speech`_ API enables developers to convert audio to text.
The API recognizes over 80 languages and variants, to support your global user base.

.. warning::

   This is a Beta release of Google Speech API. This
   API is not intended for real-time usage in critical applications.

.. _Google Speech: https://cloud.google.com/speech/docs/getting-started

Client
------

:class:`~google.cloud.speech.client.Client` objects provide a
means to configure your application. Each instance holds
an authenticated connection to the Natural Language service.

For an overview of authentication in ``google-cloud-python``, see
:doc:`google-cloud-auth`.

Assuming your environment is set up as described in that document,
create an instance of :class:`~google.cloud.speech.client.Client`.

  .. code-block:: python

     >>> from google.cloud import speech
     >>> client = speech.Client()

Methods
-------

At this moment we only support one method of the Speech API:

- `syncrecognize`_

Synchronous Recognize
---------------------

The :meth:`~google.cloud.speech.Client.syncrecognize` method
does speech to text on a file and returns the text
as a :class:`list` of tuples dicts (each containing a transcript an a confidence value).

  .. code-block:: python

     >>> alternatives = client.syncrecognize(None,"gs://my-bucket/recording.flac",
     ...                 "FLAC", 16000, max_alternatives=2):
     >>> for alternative in alternatives:
     ...     print('=' * 20)
     ...     print('   transcript: %s' % (alternative["transcript"],))
     ...     print('   confidence: %s' % (alternative["confidence"],))
     ====================
              transcript: Hello, this is a test
              confidence: 0.81
     ====================
              transcript: Hello, this is one test
              confidence: 0

.. _syncrecognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/syncrecognize
