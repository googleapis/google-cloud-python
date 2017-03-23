Using the API
=============

The `Google Natural Language`_ API can be used to reveal the
structure and meaning of text via powerful machine
learning models. You can use it to extract information about
people, places, events and much more, mentioned in text documents,
news articles or blog posts. You can use it to understand
sentiment about your product on social media or parse intent from
customer conversations happening in a call center or a messaging
app. You can analyze text uploaded in your request or integrate
with your document storage on Google Cloud Storage.

.. warning::

   This is a Beta release of Google Cloud Natural Language API. This
   API is not intended for real-time usage in critical applications.

.. _Google Natural Language: https://cloud.google.com/natural-language/docs/getting-started

Client
------

:class:`~google.cloud.language.client.Client` objects provide a
means to configure your application. Each instance holds
an authenticated connection to the Natural Language service.

For an overview of authentication in ``google-cloud-python``, see
:doc:`google-cloud-auth`.

Assuming your environment is set up as described in that document,
create an instance of :class:`~google.cloud.language.client.Client`.

  .. code-block:: python

     >>> from google.cloud import language
     >>> client = language.Client()

By default the ``language`` is ``'en-US'`` and the ``encoding`` is
UTF-8. To over-ride these values:

  .. code-block:: python

     >>> client = language.Client(language='es',
     ...                          encoding=language.Encoding.UTF16)

The encoding can be one of
:attr:`Encoding.UTF8 <google.cloud.language.document.Encoding.UTF8>`,
:attr:`Encoding.UTF16 <google.cloud.language.document.Encoding.UTF16>`, or
:attr:`Encoding.UTF32 <google.cloud.language.document.Encoding.UTF32>`.

Methods
-------

The Google Natural Language API has three supported methods

- `analyzeEntities`_
- `analyzeSentiment`_
- `annotateText`_

and each method uses a `Document`_ for representing text. To
create a :class:`~google.cloud.language.document.Document`,

  .. code-block:: python

     >>> text_content = (
     ...     'Google, headquartered in Mountain View, unveiled the '
     ...     'new Android phone at the Consumer Electronic Show.  '
     ...     'Sundar Pichai said in his keynote that users love '
     ...     'their new Android phones.')
     >>> document = client.document_from_text(text_content)

By using :meth:`~google.cloud.language.client.Client.document_from_text`,
the document's type is plain text:

  .. code-block:: python

     >>> document.doc_type == language.Document.PLAIN_TEXT
     True

The document's language defaults to ``None``, which will cause the API to
auto-detect the language.

In addition, the
:meth:`~google.cloud.language.client.Client.document_from_html`,
factory can be used to created an HTML document. In this
method and the from text method, the language can be
over-ridden:

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
     >>> document = client.document_from_html(html_content,
     ...                                      language='es')

The ``language`` argument can be either ISO-639-1 or BCP-47 language
codes; at the time, only English, Spanish, and Japanese `are supported`_.
However, the ``analyzeSentiment`` method `only supports`_ English text.

.. _are supported: https://cloud.google.com/natural-language/docs/
.. _only supports: https://cloud.google.com/natural-language/docs/reference/rest/v1beta1/documents/analyzeSentiment#body.request_body.FIELDS.document

The document type (``doc_type``) value can be one of
:attr:`Document.PLAIN_TEXT <google.cloud.language.document.Document.PLAIN_TEXT>` or
:attr:`Document.HTML <google.cloud.language.document.Document.HTML>`.

In addition to supplying the text / HTML content, a document can refer
to content stored in `Google Cloud Storage`_. We can use the
:meth:`~google.cloud.language.client.Client.document_from_url` method:

  .. code-block:: python

     >>> gcs_url = 'gs://my-text-bucket/sentiment-me.txt'
     >>> document = client.document_from_url(
     ...     gcs_url, doc_type=language.Document.HTML)
     >>> document.gcs_url == gcs_url
     True
     >>> document.doc_type == language.Document.PLAIN_TEXT
     True

The document type can be specified with the ``doc_type`` argument:

  .. code-block:: python

     >>> document = client.document_from_url(
     ...     gcs_url, doc_type=language.Document.HTML)

.. _analyzeEntities: https://cloud.google.com/natural-language/docs/reference/rest/v1beta1/documents/analyzeEntities
.. _analyzeSentiment: https://cloud.google.com/natural-language/docs/reference/rest/v1beta1/documents/analyzeSentiment
.. _annotateText: https://cloud.google.com/natural-language/docs/reference/rest/v1beta1/documents/annotateText
.. _Document: https://cloud.google.com/natural-language/reference/rest/v1beta1/Document
.. _Google Cloud Storage: https://cloud.google.com/storage/

Analyze Entities
----------------

The :meth:`~google.cloud.language.document.Document.analyze_entities` method
finds named entities (i.e. proper names) in the text and returns them
as a :class:`list` of :class:`~google.cloud.language.entity.Entity` objects.
Each entity has a corresponding type, salience (prominence), associated
metadata and other properties.

  .. code-block:: python

     >>> text_content = ("Michelangelo Caravaggio, Italian painter, is "
     ...                 "known for 'The Calling of Saint Matthew'.")
     >>> document = client.document(text_content)
     >>> entity_response = document.analyze_entities()
     >>> for entity in entity_response.entities:
     ...     print('=' * 20)
     ...     print('         name: %s' % (entity.name,))
     ...     print('         type: %s' % (entity.entity_type,))
     ...     print('     metadata: %s' % (entity.metadata,))
     ...     print('     salience: %s' % (entity.salience,))
     ====================
              name: Michelangelo Caravaggio
              type: PERSON
          metadata: {'wikipedia_url': 'http://en.wikipedia.org/wiki/Caravaggio'}
          salience: 0.7615959
     ====================
              name: Italian
              type: LOCATION
          metadata: {'wikipedia_url': 'http://en.wikipedia.org/wiki/Caravaggio'}
          salience: 0.19960518
     ====================
              name: The Calling of Saint Matthew
              type: EVENT
          metadata: {'wikipedia_url': 'http://en.wikipedia.org/wiki/Caravaggio'}
          salience: 0.038798928

Analyze Sentiment
-----------------

The :meth:`~google.cloud.language.document.Document.analyze_sentiment` method
analyzes the sentiment of the provided text and returns a
:class:`~google.cloud.language.sentiment.Sentiment`. Currently, this method
only supports English text.

  .. code-block:: python

     >>> text_content = "Jogging isn't very fun."
     >>> document = client.document(text_content)
     >>> sentiment_response = document.analyze_sentiment()
     >>> sentiment = sentiment_response.sentiment
     >>> print(sentiment.score)
     -1
     >>> print(sentiment.magnitude)
     0.8

Annotate Text
-------------

The :meth:`~google.cloud.language.document.Document.annotate_text` method
analyzes a document and is intended for users who are familiar with
machine learning and need in-depth text features to build upon.

The method returns a named tuple with four entries:

* ``sentences``: A :class:`list` of sentences in the text
* ``tokens``: A :class:`list` of :class:`~google.cloud.language.syntax.Token`
  object (e.g. words, punctuation)
* ``sentiment``: The :class:`~google.cloud.language.sentiment.Sentiment` of
  the text (as returned by
  :meth:`~google.cloud.language.document.Document.analyze_sentiment`)
* ``entities``: :class:`list` of :class:`~google.cloud.language.entity.Entity`
  objects extracted from the text (as returned by
  :meth:`~google.cloud.language.document.Document.analyze_entities`)

By default :meth:`~google.cloud.language.document.Document.annotate_text` has
three arguments ``include_syntax``, ``include_entities`` and
``include_sentiment`` which are all :data:`True`. However, each of these
`Features`_ can be selectively turned off by setting the corresponding
arguments to :data:`False`.

When ``include_syntax=False``, ``sentences`` and ``tokens`` in the
response is :data:`None`. When ``include_sentiment=False``, ``sentiment`` in
the response is :data:`None`. When ``include_entities=False``, ``entities`` in
the response is :data:`None`.

  .. code-block:: python

     >>> text_content = 'The cow jumped over the Moon.'
     >>> document = client.document(text_content)
     >>> annotations = document.annotate_text()
     >>> # Sentences present if include_syntax=True
     >>> print(annotations.sentences)
     ['The cow jumped over the Moon.']
     >>> # Tokens present if include_syntax=True
     >>> for token in annotations.tokens:
     ...     msg = '%11s: %s' % (token.part_of_speech, token.text_content)
     ...     print(msg)
      DETERMINER: The
            NOUN: cow
            VERB: jumped
      ADPOSITION: over
      DETERMINER: the
            NOUN: Moon
     PUNCTUATION: .
     >>> # Sentiment present if include_sentiment=True
     >>> print(annotations.sentiment.score)
     1
     >>> print(annotations.sentiment.magnitude)
     0.1
     >>> # Entities present if include_entities=True
     >>> for entity in annotations.entities:
     ...     print('=' * 20)
     ...     print('         name: %s' % (entity.name,))
     ...     print('         type: %s' % (entity.entity_type,))
     ...     print('     metadata: %s' % (entity.metadata,))
     ...     print('     salience: %s' % (entity.salience,))
     ====================
              name: Moon
              type: LOCATION
          metadata: {'wikipedia_url': 'http://en.wikipedia.org/wiki/Natural_satellite'}
          salience: 0.11793101

.. _Features: https://cloud.google.com/natural-language/docs/reference/rest/v1beta1/documents/annotateText#Features
