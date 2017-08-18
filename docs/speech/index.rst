######
Speech
######

The `Google Speech`_ API enables developers to convert audio to text.
The API recognizes over 80 languages and variants, to support your global user
base.

.. _Google Speech: https://cloud.google.com/speech/docs/getting-started


Authentication and Configuration
--------------------------------

:class:`~google.cloud.speech_v1.SpeechClient` objects provide a
means to configure your application. Each instance holds
an authenticated connection to the Cloud Speech Service.

For an overview of authentication in ``google-cloud-python``, see
:doc:`/core/auth`.

Assuming your environment is set up as described in that document,
create an instance of :class:`~.speech_v1.SpeechClient`.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.SpeechClient()


Asynchronous Recognition
------------------------

The :meth:`~.speech_v1.SpeechClient.long_running_recognize` method
sends audio data to the Speech API and initiates a Long Running Operation.

Using this operation, you can periodically poll for recognition results.
Use asynchronous requests for audio data of any duration up to 80 minutes.

See: `Speech Asynchronous Recognize`_


.. code-block:: python

    >>> import time
    >>> from google.cloud import speech
    >>> client = speech.SpeechClient()
    >>> operation = client.long_running_recognize(
    ...     audio=speech.types.RecognitionAudio(
    ...         uri='gs://my-bucket/recording.flac',
    ...     ),
    ...     config=speech.types.RecognitionConfig(
    ...         encoding='LINEAR16',
    ...         language_code='en-US',
    ...         sample_rate_hertz=44100,
    ...     ),
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

The :meth:`~.speech_v1.SpeechClient.recognize` method converts speech
data to text and returns alternative text transcriptions.

This example uses ``language_code='en-GB'`` to better recognize a dialect from
Great Britain.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.SpeechClient()
    >>> results = client.recognize(
    ...     audio=speech.types.RecognitionAudio(
    ...         uri='gs://my-bucket/recording.flac',
    ...     ),
    ...     config=speech.types.RecognitionConfig(
    ...         encoding='LINEAR16',
    ...         language_code='en-US',
    ...         sample_rate_hertz=44100,
    ...     ),
    ... )
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
    >>> client = speech.SpeechClient()
    >>> results = client.recognize(
    ...     audio=speech.types.RecognitionAudio(
    ...         uri='gs://my-bucket/recording.flac',
    ...     ),
    ...     config=speech.types.RecognitionConfig(
    ...         encoding='LINEAR16',
    ...         language_code='en-US',
    ...         profanity_filter=True,
    ...         sample_rate_hertz=44100,
    ...     ),
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
    >>> from google.cloud import speech
    >>> client = speech.SpeechClient()
    >>> results = client.recognize(
    ...     audio=speech.types.RecognitionAudio(
    ...         uri='gs://my-bucket/recording.flac',
    ...     ),
    ...     config=speech.types.RecognitionConfig(
    ...         encoding='LINEAR16',
    ...         language_code='en-US',
    ...         sample_rate_hertz=44100,
    ...         speech_contexts=[speech.types.SpeechContext(
    ...             phrases=['hi', 'good afternoon'],
    ...         )],
    ...     ),
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

The :meth:`~speech_v1.SpeechClient.streaming_recognize` method converts
speech data to possible text alternatives on the fly.

.. note::
    Streaming recognition requests are limited to 1 minute of audio.

    See: https://cloud.google.com/speech/limits#content

.. code-block:: python

    >>> import io
    >>> from google.cloud import speech
    >>> client = speech.SpeechClient()
    >>> config = speech.types.RecognitionConfig(
    ...     encoding='LINEAR16',
    ...     language_code='en-US',
    ...     sample_rate_hertz=44100,
    ... )
    >>> with io.open('./hello.wav', 'rb') as stream:
    ...     requests = [speech.types.StreamingRecognizeRequest(
    ...         audio_content=stream.read(),
    ...     )]
    >>> results = sample.streaming_recognize(
    ...     config=speech.types.StreamingRecognitionConfig(config=config),
    ...     requests,
    ... )
    >>> for result in results:
    ...     for alternative in result.alternatives:
    ...         print('=' * 20)
    ...         print('transcript: ' + alternative.transcript)
    ...         print('confidence: ' + str(alternative.confidence))
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

    >>> import io
    >>> from google.cloud import speech
    >>> client = speech.SpeechClient()
    >>> config = speech.types.RecognitionConfig(
    ...     encoding='LINEAR16',
    ...     language_code='en-US',
    ...     sample_rate_hertz=44100,
    ... )
    >>> with io.open('./hello-pause-goodbye.wav', 'rb') as stream:
    ...     requests = [speech.types.StreamingRecognizeRequest(
    ...         audio_content=stream.read(),
    ...     )]
    >>> results = sample.streaming_recognize(
    ...     config=speech.types.StreamingRecognitionConfig(
    ...         config=config,
    ...         single_utterance=False,
    ...     ),
    ...     requests,
    ... )
    >>> for result in results:
    ...     for alternative in result.alternatives:
    ...         print('=' * 20)
    ...         print('transcript: ' + alternative.transcript)
    ...         print('confidence: ' + str(alternative.confidence))
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

    >>> import io
    >>> from google.cloud import speech
    >>> client = speech.SpeechClient()
    >>> config = speech.types.RecognitionConfig(
    ...     encoding='LINEAR16',
    ...     language_code='en-US',
    ...     sample_rate_hertz=44100,
    ... )
    >>> with io.open('./hello.wav', 'rb') as stream:
    ...     requests = [speech.types.StreamingRecognizeRequest(
    ...         audio_content=stream.read(),
    ...     )]
    >>> config = speech.types.StreamingRecognitionConfig(config=config)
    >>> responses = client.streaming_recognize(config,requests)
    >>> for response in responses:
    ...     for result in response:
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


API Reference
-------------

.. toctree::
  :maxdepth: 2

  gapic/api
  gapic/types
