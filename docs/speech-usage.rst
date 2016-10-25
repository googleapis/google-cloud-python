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
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.FLAC,
    ...                        sample_rate=44100)
    >>> operation = client.async_recognize(sample, max_alternatives=2)
    >>> alternatives = client.sync_recognize(
    ...     speech.Encoding.FLAC, 16000,
    ...     source_uri='gs://my-bucket/recording.flac', language_code='en-GB',
    ...     max_alternatives=2)
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
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.FLAC,
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
    >>> client = speech.Client()
    >>> sample = client.sample(source_uri='gs://my-bucket/recording.flac',
    ...                        encoding=speech.Encoding.FLAC,
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

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> with open('./hello.wav', 'rb') as stream:
    ...     sample = client.sample(stream=stream, encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate=16000)
    ...     for response in client.stream_recognize(sample):
    ...         print(response.transcript)
    ...         print(response.is_final)
    hello
    True


By setting ``interim_results`` to :data:`True`, interim results (tentative hypotheses)
may be returned as they become available (these interim results are indicated
with the ``is_final=false`` flag). If :data:`False` or omitted, only ``is_final=true``
result(s) are returned.

.. code-block:: python

    >>> from google.cloud import speech
    >>> client = speech.Client()
    >>> with open('./hello.wav', 'rb') as stream:
    ...     sample = client.sample(stream=stream, encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate=16000)
    ...     for response in client.stream_recognize(sample,
    ...                                             interim_results=True):
    ...         print('====Response====')
    ...         print(response.transcript)
    ...         print(response.is_final)
    ====Response====
    he
    False
    ====Response====
    hell
    False
    ====Repsonse====
    hello
    True


By default the recognizer will perform continuous recognition
(continuing to process audio even if the user pauses speaking) until the client
closes the output stream or when the maximum time limit has been reached.

If you only want to recognize a single utterance you can set
 ``single_utterance`` to ``True`` and only one result will be returned.

See: `Single Utterance`_

.. code-block:: python

    >>> with open('./hello_pause_goodbye.wav', 'rb') as stream:
    ...     sample = client.sample(stream=stream, encoding=speech.Encoding.LINEAR16,
    ...                            sample_rate=16000)
    ...     for response in client.stream_recognize(sample,
    ...                                             single_utterance=True):
    ...         print(response.transcript)
    ...         print(response.is_final)
    hello
    True

.. _Single Utterance: https://cloud.google.com/speech/reference/rpc/google.cloud.speech.v1beta1#streamingrecognitionconfig
.. _sync_recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/syncrecognize
.. _Speech Asynchronous Recognize: https://cloud.google.com/speech/reference/rest/v1beta1/speech/asyncrecognize
