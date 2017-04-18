Using the API
=============

The `Google Speech`_ API enables developers to convert audio to text.
The API recognizes over 80 languages and variants, to support your global user
base.

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


Asynchronous Recognition
------------------------

The :meth:`~google.cloud.speech.Client.long_running_recognize` sends audio
data to the Speech API and initiates a Long Running Operation. Using this
operation, you can periodically poll for recognition results. Use asynchronous
requests for audio data of any duration up to 80 minutes.

See: `Speech Asynchronous Recognize`_


.. code-block:: python

    >>> import time
    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.LINEAR16,
    ...                        sample_rate_hertz=44100)
    >>> operation = sample.long_running_recognize(
    ...     language_code='en-US',
    ...     max_alternatives=2,
    ... )
    >>> retry_count = 100
    >>> while retry_count > 0 and not operation.complete:
    ...     retry_count -= 1
    ...     time.sleep(10)
    ...     operation.poll()  # API call
    >>> operation.complete
    True
    >>> for result in operation.results:
    ...     for alternative in result.alternatives:
    ...         print('=' * 20)
    ...         print(alternative.transcript)
    ...         print(alternative.confidence)
    ====================
    'how old is the Brooklyn Bridge'
    0.98267895


Synchronous Recognition
-----------------------

The :meth:`~google.cloud.speech.Client.recognize` method converts speech
data to text and returns alternative text transcriptions.

This example uses ``language_code='en-GB'`` to better recognize a dialect from
Great Britain.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.FLAC,
    ...                        sample_rate_hertz=44100)
    >>> results = sample.recognize(
    ...     language_code='en-GB', max_alternatives=2)
    >>> for result in results:
    ...     for alternative in result.alternatives:
    ...         print('=' * 20)
    ...         print('transcript: ' + alternative.transcript)
    ...         print('confidence: ' + str(alternative.confidence))
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
    ...                        sample_rate_hertz=44100)
    >>> results = sample.recognize(
    ...     language_code='en-US',
    ...     max_alternatives=1,
    ...     profanity_filter=True,
    ... )
    >>> for result in results:
    ...     for alternative in result.alternatives:
    ...         print('=' * 20)
    ...         print('transcript: ' + alternative.transcript)
    ...         print('confidence: ' + str(alternative.confidence))
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
    ...                        sample_rate_hertz=44100)
    >>> hints = ['hi', 'good afternoon']
    >>> results = sample.recognize(
    ...     language_code='en-US',
    ...     max_alternatives=2,
    ...     speech_context=hints,
    ... )
    >>> for result in results:
    ...     for alternative in result.alternatives:
    ...         print('=' * 20)
    ...         print('transcript: ' + alternative.transcript)
    ...         print('confidence: ' + str(alternative.confidence))
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
    ...     sample = client.sample(stream=stream,
    ...                            encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate_hertz=16000)
    ...     results = sample.streaming_recognize(language_code='en-US')
    ...     for result in results:
    ...         for alternative in result.alternatives:
    ...             print('=' * 20)
    ...             print('transcript: ' + alternative.transcript)
    ...             print('confidence: ' + str(alternative.confidence))
    ====================
    transcript: hello thank you for using Google Cloud platform
    confidence: 0.927983105183


By default the API will perform continuous recognition
(continuing to process audio even if the speaker in the audio pauses speaking)
until the client closes the output stream or until the maximum time limit has
been reached.

If you only want to recognize a single utterance you can set
 ``single_utterance`` to :data:`True` and only one result will be returned.

See: `Single Utterance`_

.. code-block:: python

    >>> with open('./hello_pause_goodbye.wav', 'rb') as stream:
    ...     sample = client.sample(stream=stream,
    ...                            encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate_hertz=16000)
    ...     results = sample.streaming_recognize(
    ...         language_code='en-US',
    ...         single_utterance=True,
    ...     )
    ...     for result in results:
    ...         for alternative in result.alternatives:
    ...             print('=' * 20)
    ...             print('transcript: ' + alternative.transcript)
    ...             print('confidence: ' + str(alternative.confidence))
    ====================
    transcript: testing a pause
    confidence: 0.933770477772

If ``interim_results`` is set to :data:`True`, interim results
(tentative hypotheses) may be returned as they become available.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> with open('./hello.wav', 'rb') as stream:
    ...     sample = client.sample(stream=stream,
    ...                            encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate=16000)
    ...     results = sample.streaming_recognize(
    ...         interim_results=True,
    ...         language_code='en-US',
    ...     )
    ...     for result in results:
    ...         for alternative in result.alternatives:
    ...             print('=' * 20)
    ...             print('transcript: ' + alternative.transcript)
    ...             print('confidence: ' + str(alternative.confidence))
    ...             print('is_final:' + str(result.is_final))
    ====================
    'he'
    None
    False
    ====================
    'hell'
    None
    False
    ====================
    'hello'
    0.973458576
    True


.. _Single Utterance: https://cloud.google.com/speech/reference/rpc/google.cloud.speech.v1beta1#streamingrecognitionconfig
.. _sync_recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/syncrecognize
.. _Speech Asynchronous Recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/asyncrecognize
