Using the API
=============

The `Google Speech`_ API enables developers to convert audio to text.
The API recognizes over 80 languages and variants, to support your global user
base.

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


Asychronous Recognition
-----------------------

The :meth:`~google.cloud.speech.Client.async_recognize` sends audio data to the
Speech API and initiates a Long Running Operation. Using this operation, you
can periodically poll for recognition results. Use asynchronous requests for
audio data of any duration up to 80 minutes.

See: `Speech Asynchronous Recognize`_


.. code-block:: python

    >>> import time
    >>> from google.cloud import speech
    >>> from google.cloud.speech.encoding import Encoding
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> operation = client.async_recognize(sample, max_alternatives=2)
    >>> retry_count = 100
    >>> while retry_count > 0 and not operation.complete:
    ...     retry_count -= 1
    ...     time.sleep(10)
    ...     operation.poll()  # API call
    >>> operation.complete
    True
    >>> operation.results[0].transcript
    'how old is the Brooklyn Bridge'
    >>> operation.results[0].confidence
    0.98267895


Synchronous Recognition
-----------------------

The :meth:`~google.cloud.speech.Client.sync_recognize` method converts speech
data to text and returns alternative text transcriptons.

This example uses ``language_code='en-GB'`` to better recognize a dialect from
Great Britian.

.. code-block:: python

    >>> from google.cloud import speech
    >>> from google.cloud.speech.encoding import Encoding
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> operation = client.async_recognize(sample, max_alternatives=2)
     >>> alternatives = client.sync_recognize(
     ...     'FLAC', 16000, source_uri='gs://my-bucket/recording.flac',
     ...     language_code='en-GB', max_alternatives=2)
     >>> for alternative in alternatives:
     ...     print('=' * 20)
     ...     print('transcript: ' + alternative['transcript'])
     ...     print('confidence: ' + alternative['confidence'])
     ====================
     transcript: Hello, this is a test
     confidence: 0.81
     ====================
     transcript: Hello, this is one test
     confidence: 0


Example of using the profanity filter.

.. code-block:: python

    >>> from google.cloud import speech
    >>> from google.cloud.speech.encoding import Encoding
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> alternatives = client.sync_recognize(sample, max_alternatives=1,
    ...                                      profanity_filter=True)
    >>> for alternative in alternatives:
    ...     print('=' * 20)
    ...     print('transcript: ' + alternative['transcript'])
    ...     print('confidence: ' + alternative['confidence'])
    ====================
    transcript: Hello, this is a f****** test
    confidence: 0.81

Using speech context hints to get better results. This can be used to improve
the accuracy for specific words and phrases. This can also be used to add new
words to the vocabulary of the recognizer.

.. code-block:: python

    >>> from google.cloud import speech
    >>> from google.cloud.speech.encoding import Encoding
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> hints = ['hi', 'good afternoon']
    >>> alternatives = client.sync_recognize(sample, max_alternatives=2,
    ...                                      speech_context=hints)
    >>> for alternative in alternatives:
    ...     print('=' * 20)
    ...     print('transcript: ' + alternative['transcript'])
    ...     print('confidence: ' + alternative['confidence'])
    ====================
    transcript: Hello, this is a test
    confidence: 0.81


Streaming Recognition
---------------------

The :meth:`~google.cloud.speech.Client.stream_recognize` method converts speech
data to possible text alternatives on the fly.

.. note::
    Streaming recognition requests are limited to 1 minute of audio.

    See: https://cloud.google.com/speech/limits#content


    >>> from google.cloud import speech
    >>> from google.cloud.speech.encoding import Encoding
    >>> client = speech.Client()
    >>> with open('hello.flac', 'rb') as content:
    >>>     sample = client.sample(content=content.read(),
    ...                            encoding=Encoding.FLAC,
    ...                            sample_rate=44100)
    >>>     results = client.stream_recognize(sample)
    >>> results[0].is_final
    False
    >>> results[2].is_final
    True
    >>> results[2].alternatives[0].transcript
    hello
    >>> results[2].alternatives[0].confidence
    0.96976006031

For continuous speech containing more than one word, the ``single_utterance``
option should be disabled.

See: `Single Utterance`_

.. code-block:: python

    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> results = client.stream_recognize(sample, single_utterance=False)


If you would like interim results to be returned as well as the final results,
you can set the ``interim_results`` option to ``True``.

  .. code-block:: python

    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> results = client.stream_recognize(sample, interim_results=True)
    >>> print results[0].alternatives.transcript
    'how'
    >>> print results[0].stability
    0.00999999977648
    >>> print results[2].alternatives.transcript
    'hello'
    >>> print results[2].alternatives.confidence
    0.96976006031
    >>> print results[2].is_final
    True


.. _Single Utterance: https://cloud.google.com/speech/reference/rpc/google.cloud.speech.v1beta1#streamingrecognitionconfig
.. _sync_recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/syncrecognize
.. _Speech Asynchronous Recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/asyncrecognize
