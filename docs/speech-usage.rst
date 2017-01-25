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

.. note::

    Only the :attr:`Encoding.LINEAR16` encoding type is supported by
    asynchronous recognition.

See: `Speech Asynchronous Recognize`_


.. code-block:: python

    >>> import time
    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.LINEAR16,
    ...                        sample_rate=44100)
    >>> operation = sample.async_recognize(max_alternatives=2)
    >>> retry_count = 100
    >>> while retry_count > 0 and not operation.complete:
    ...     retry_count -= 1
    ...     time.sleep(10)
    ...     operation.poll()  # API call
    >>> operation.complete
    True
    >>> for result in operation.results:
    ...     print('=' * 20)
    ...     print(result.transcript)
    ...     print(result.confidence)
    ====================
    'how old is the Brooklyn Bridge'
    0.98267895


Synchronous Recognition
-----------------------

The :meth:`~google.cloud.speech.Client.sync_recognize` method converts speech
data to text and returns alternative text transcriptons.

This example uses ``language_code='en-GB'`` to better recognize a dialect from
Great Britian.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> results = sample.sync_recognize(
    ...     speech.Encoding.FLAC, 16000,
    ...     source_uri='gs://my-bucket/recording.flac', language_code='en-GB',
    ...     max_alternatives=2)
    >>> for result in results:
    ...     print('=' * 20)
    ...     print('transcript: ' + result.transcript)
    ...     print('confidence: ' + result.confidence)
    ====================
    transcript: Hello, this is a test
    confidence: 0.81
    ====================
    transcript: Hello, this is one test
    confidence: 0

Example of using the profanity filter.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> results = sample.sync_recognize(max_alternatives=1,
    ...                                 profanity_filter=True)
    >>> for result in results:
    ...     print('=' * 20)
    ...     print('transcript: ' + result.transcript)
    ...     print('confidence: ' + result.confidence)
    ====================
    transcript: Hello, this is a f****** test
    confidence: 0.81

Using speech context hints to get better results. This can be used to improve
the accuracy for specific words and phrases. This can also be used to add new
words to the vocabulary of the recognizer.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> hints = ['hi', 'good afternoon']
    >>> results = sample.sync_recognize(max_alternatives=2,
    ...                                 speech_context=hints)
    >>> for result in results:
    ...     print('=' * 20)
    ...     print('transcript: ' + result.transcript)
    ...     print('confidence: ' + result.confidence)
    ====================
    transcript: Hello, this is a test
    confidence: 0.81


Streaming Recognition
---------------------

The :meth:`~google.cloud.speech.Client.streaming_recognize` method converts
speech data to possible text alternatives on the fly.

.. note::
    Streaming recognition requests are limited to 1 minute of audio.

    See: https://cloud.google.com/speech/limits#content

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> with open('./hello.wav', 'rb') as stream:
    ...     sample = client.sample(content=stream,
    ...                            encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate=16000)
    ...     results = list(sample.streaming_recognize())
    >>> print(results[0].alternatives[0].transcript)
    'hello'
    >>> print(results[0].alternatives[0].confidence)
    0.973458576


By default the API will perform continuous recognition
(continuing to process audio even if the speaker in the audio pauses speaking)
until the client closes the output stream or until the maximum time limit has
been reached.

If you only want to recognize a single utterance you can set
 ``single_utterance`` to :data:`True` and only one result will be returned.

See: `Single Utterance`_

.. code-block:: python

    >>> with open('./hello_pause_goodbye.wav', 'rb') as stream:
    ...     sample = client.sample(content=stream,
    ...                            encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate=16000)
    ...     responses = sample.streaming_recognize(single_utterance=True)
    ...     results = list(responses)
    >>> print(results[0].alternatives[0].transcript)
    hello
    >>> print(results[0].alternatives[0].confidence)
    0.96523453546


If ``interim_results`` is set to :data:`True`, interim results
(tentative hypotheses) may be returned as they become available.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> with open('./hello.wav', 'rb') as stream:
    ...     sample = client.sample(content=stream,
    ...                            encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate=16000)
    ...     for results in sample.streaming_recognize(interim_results=True):
    ...         print('=' * 20)
    ...         print(results[0].alternatives[0].transcript)
    ...         print(results[0].alternatives[0].confidence)
    ...         print(results[0].is_final)
    ...         print(results[0].stability)
    ====================
    'he'
    None
    False
    0.113245
    ====================
    'hell'
    None
    False
    0.132454
    ====================
    'hello'
    0.973458576
    True
    0.982345


.. _Single Utterance: https://cloud.google.com/speech/reference/rpc/google.cloud.speech.v1beta1#streamingrecognitionconfig
.. _sync_recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/syncrecognize
.. _Speech Asynchronous Recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/asyncrecognize
