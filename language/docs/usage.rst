Using the Language Client
=========================

Documents
*********

The Google Natural Language API has the following supported methods:

- `analyzeEntities`_
- `analyzeSentiment`_
- `analyzeEntitySentiment`_
- `annotateText`_
- `classifyText`_

and each method uses a :class:`~.language_v1.types.Document` for representing
text.

  .. code-block:: python

      >>> document = language.types.Document(
      ...     content='Google, headquartered in Mountain View, unveiled the '
      ...             'new Android phone at the Consumer Electronic Show.  '
      ...             'Sundar Pichai said in his keynote that users love '
      ...             'their new Android phones.',
      ...     language='en',
      ...     type='PLAIN_TEXT',
      ... )


The document's language defaults to ``None``, which will cause the API to
auto-detect the language.

In addition, you can construct an HTML document:

  .. code-block:: python

      >>> html_content = """\
      ... <html>
      ...   <head>
      ...     <title>El Tiempo de las Historias</time>
      ...   </head>
      ...   <body>
      ...     <p>La vaca salt&oacute; sobre la luna.</p>
      ...   </body>
      ... </html>
      ... """
      >>> document = language.types.Document(
      ...     content=html_content,
      ...     language='es',
      ...     type='HTML',
      ... )

The ``language`` argument can be either ISO-639-1 or BCP-47 language
codes. The API reference page contains the full list of `supported languages`_.

.. _supported languages: https://cloud.google.com/natural-language/docs/languages


In addition to supplying the text / HTML content, a document can refer
to content stored in `Google Cloud Storage`_.

  .. code-block:: python

     >>> document = language.types.Document(
     ...     gcs_content_uri='gs://my-text-bucket/sentiment-me.txt',
     ...     type=language.enums.HTML,
     ... )

.. _analyzeEntities: https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeEntities
.. _analyzeSentiment: https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeSentiment
.. _analyzeEntitySentiment: https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/analyzeEntitySentiment
.. _annotateText: https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/annotateText
.. _classifyText: https://cloud.google.com/natural-language/docs/reference/rest/v1/documents/classifyText
.. _Google Cloud Storage: https://cloud.google.com/storage/

Analyze Entities
****************

The :meth:`~.language_v1.LanguageServiceClient.analyze_entities`
method finds named entities (i.e. proper names) in the text. This method
returns a :class:`~.language_v1.types.AnalyzeEntitiesResponse`.

  .. code-block:: python

     >>> document = language.types.Document(
     ...     content='Michelangelo Caravaggio, Italian painter, is '
     ...             'known for "The Calling of Saint Matthew".',
     ...     type=language.enums.Document.Type.PLAIN_TEXT,
     ... )
     >>> response = client.analyze_entities(
     ...     document=document,
     ...     encoding_type='UTF32',
     ... )
     >>> for entity in response.entities:
     ...     print('=' * 20)
     ...     print('         name: {0}'.format(entity.name))
     ...     print('         type: {0}'.format(entity.type))
     ...     print('     metadata: {0}'.format(entity.metadata))
     ...     print('     salience: {0}'.format(entity.salience))
     ====================
              name: Michelangelo Caravaggio
              type: PERSON
          metadata: {'wikipedia_url': 'https://en.wikipedia.org/wiki/Caravaggio'}
          salience: 0.7615959
     ====================
              name: Italian
              type: LOCATION
          metadata: {'wikipedia_url': 'https://en.wikipedia.org/wiki/Italy'}
          salience: 0.19960518
     ====================
              name: The Calling of Saint Matthew
              type: EVENT
          metadata: {'wikipedia_url': 'https://en.wikipedia.org/wiki/The_Calling_of_St_Matthew_(Caravaggio)'}
          salience: 0.038798928

.. note::

  It is recommended to send an ``encoding_type`` argument to Natural
  Language methods, so they provide useful offsets for the data they return.
  While the correct value varies by environment, in Python you *usually*
  want ``UTF32``.


Analyze Sentiment
*****************

The :meth:`~.language_v1.LanguageServiceClient.analyze_sentiment` method
analyzes the sentiment of the provided text. This method returns a
:class:`~.language_v1.types.AnalyzeSentimentResponse`.

  .. code-block:: python

     >>> document = language.types.Document(
     ...     content='Jogging is not very fun.',
     ...     type='PLAIN_TEXT',
     ... )
     >>> response = client.analyze_sentiment(
     ...     document=document,
     ...     encoding_type='UTF32',
     ... )
     >>> sentiment = response.document_sentiment
     >>> print(sentiment.score)
     -1
     >>> print(sentiment.magnitude)
     0.8

.. note::

  It is recommended to send an ``encoding_type`` argument to Natural
  Language methods, so they provide useful offsets for the data they return.
  While the correct value varies by environment, in Python you *usually*
  want ``UTF32``.


Analyze Entity Sentiment
************************

The :meth:`~.language_v1.LanguageServiceClient.analyze_entity_sentiment`
method is effectively the amalgamation of
:meth:`~.language_v1.LanguageServiceClient.analyze_entities` and
:meth:`~.language_v1.LanguageServiceClient.analyze_sentiment`.
This method returns a
:class:`~.language_v1.types.AnalyzeEntitySentimentResponse`.

.. code-block:: python

    >>> document = language.types.Document(
    ...     content='Mona said that jogging is very fun.',
    ...     type='PLAIN_TEXT',
    ... )
    >>> response = client.analyze_entity_sentiment(
    ...     document=document,
    ...     encoding_type='UTF32',
    ... )
    >>> entities = response.entities
    >>> entities[0].name
    'Mona'
    >>> entities[1].name
    'jogging'
    >>> entities[1].sentiment.magnitude
    0.8
    >>> entities[1].sentiment.score
    0.8

.. note::

    It is recommended to send an ``encoding_type`` argument to Natural
    Language methods, so they provide useful offsets for the data they return.
    While the correct value varies by environment, in Python you *usually*
    want ``UTF32``.


Annotate Text
*************

The :meth:`~.language_v1.LanguageServiceClient.annotate_text` method
analyzes a document and is intended for users who are familiar with
machine learning and need in-depth text features to build upon. This method
returns a :class:`~.language_v1.types.AnnotateTextResponse`.
