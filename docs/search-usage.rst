Using the API
=============

Overview
~~~~~~~~

Cloud Search allows an application to quickly perform full-text and
geospatial searches without having to spin up instances
and without the hassle of managing and maintaining a search service.

Cloud Search provides a model for indexing documents containing structured data,
with documents and indexes saved to a separate persistent store optimized
for search operations.

The API supports full text matching on string fields and allows indexing
any number of documents in any number of indexes.

.. note::

   The Google Cloud Search API is an alpha API. To use it, accounts must
   be whitelisted.

Client
------

:class:`Client <gcloud.search.client.Client>` objects provide a means to
configure your Cloud Search applications.  Eash instance holds both a
``project`` and an authenticated connection to the Cloud Search service.

For an overview of authentication in ``gcloud-python``, see :doc:`gcloud-auth`.

Assuming your environment is set up as described in that document,
create an instance of :class:`Client <gcloud.search.client.Client>`.

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()

Indexes
~~~~~~~

Indexes are searchable collections of documents.

List all indexes in the client's project:

.. doctest::

   >>> indexes = client.list_indexes()  # API call
   >>> for index in indexes:
   ...     print(index.name)
   ...     field_names = ', '.join([field.name for field in index.fields])
   ...     print('- %s' % field_names)
   index-name
   - field-1, field-2
   another-index-name
   - field-3

Create a new index:

.. doctest::

   >>> new_index = client.index('new-index-name')

.. note::

   Indexes cannot be created, updated, or deleted directly on the server:
   they are derived from the documents which are created "within" them.

Documents
~~~~~~~~~

Create a document instance, which is not yet added to its index on
the server:

.. doctest::

   >>> index = client.index('index-id')
   >>> document = index.document('document-1')
   >>> document.exists()  # API call
   False
   >>> document.rank
   None

Add one or more fields to the document:

.. doctest::

   >>> field = document.Field('fieldname')
   >>> field.add_value('string')

Save the document into the index:

.. doctest::

   >>> document.create()  # API call
   >>> document.exists()  # API call
   True
   >>> document.rank      # set by the server
   1443648166

List all documents in an index:

.. doctest::

   >>> documents = index.list_documents()  # API call
   >>> [document.id for document in documents]
   ['document-1']

Delete a document from its index:

.. doctest::

   >>> document = index.document('to-be-deleted')
   >>> document.exists()  # API call
   True
   >>> document.delete()  # API call
   >>> document.exists()  # API clal
   False

.. note::

   To update a document in place after manipulating its fields or rank, just
   recreate it:  E.g.:

   .. doctest::

      >>> document = index.document('document-id')
      >>> document.exists()  # API call
      True
      >>> document.rank = 12345
      >>> field = document.field('field-name')
      >>> field.add_value('christina aguilera')
      >>> document.create()  # API call

Fields
~~~~~~

Fields belong to documents and are the data that actually gets searched.

Each field can have multiple values, which can be of the following types:

- String (Python2 :class:`unicode`, Python3 :class:`str`)
- Number (Python :class:`int` or :class:`float`)
- Timestamp (Python :class:`datetime.datetime`)
- Geovalue (Python tuple, (:class:`float`, :class:`float`))

String values can be tokenized using one of three different types of
tokenization, which can be passed when the value is added:

- **Atom** (``atom``) means "don't tokenize this string", treat it as one
  thing to compare against.

- **Text** (``text``) means "treat this string as normal text" and split words
  apart to be compared against.

- **HTML** (``html``) means "treat this string as HTML", understanding the
  tags, and treating the rest of the content like Text.

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()
   >>> index = client.index('index-id')
   >>> document = index.document('document-id')
   >>> field = document.field('field-name')
   >>> field.add_value('britney spears', tokenization='atom')
   >>> field.add_value(''<h1>Britney Spears</h1>', tokenization='html')

Searching
~~~~~~~~~

After populating an index with documents, search through them by
issuing a search query:

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()
   >>> index = client.index('index-id')
   >>> query = client.query('britney spears')
   >>> matching_documents = index.search(query)  # API call
   >>> for document in matching_documents:
   ...     print(document.id)
   ['document-id']

By default, all queries are sorted by the ``rank`` value set when the
document was created.  See:
https://cloud.google.com/search/reference/rest/v1/projects/indexes/documents#resource_representation.google.cloudsearch.v1.Document.rank

To sort differently, use the ``order_by`` parameter:

.. doctest::

   >>> ordered = client.query('britney spears', order_by=['field1', '-field2'])

Note that the ``-`` character before ``field2`` means that this query will
be sorted ascending by ``field1`` and then descending by ``field2``.

To limit the fields to be returned in the match, use the ``fields`` paramater:

.. doctest::

   >>> projected = client.query('britney spears', fields=['field1', 'field2'])
