.. toctree::
  :maxdepth: 1
  :hidden:

Search
------

Overview
~~~~~~~~

Cloud Search allows you to quickly perform full-text and geospatial searches
against your data without having to spin up your own instances
and without the hassle of managing and maintaining a search service.

Cloud Search provides a model for indexing your documents
that contain structured data,
with documents and indexes saved to a separate persistent store
optimized for search operations.
You can search an index, and organize and present your search results.
The API supports full text matching on string fields
and allows you to index any number of documents in any number of indexes.

Indexes
~~~~~~~

Here's an example of how you might deal with indexes::

    >>> from gcloud import search
    >>> client = search.Client()

    >>> # List all indexes in your project
    >>> for index in client.list_indexes():
    ...     print index

    >>> # Create a new index
    >>> new_index = client.index('index-id-here')
    >>> new_index.name = 'My new index'
    >>> new_index.create()

    >>> # Update an existing index
    >>> index = client.get_index('existing-index-id')
    >>> print index
    <Index: Existing Index (existing-index-id)>
    >>> index.name = 'Modified name'
    >>> index.update()
    >>> print index
    <Index: Modified name (existing-index-id)>

    >>> # Delete an index
    >>> index = client.get_index('existing-index-id')
    >>> index.delete()

Documents
~~~~~~~~~

Documents are the things that you search for.
The typical process is:

#. Create a document
#. Add fields to the document
#. Add the document to an index to be searched for later

Here's an example of how you might deal with documents::

    >>> from gcloud import search
    >>> client = search.Client()

    >>> # Create a document
    >>> document = search.Document('document-id')

    >>> # Add a field to the document
    >>> field = search.Field('fieldname')
    >>> field.add_value('string')
    >>> document.add_field(field)

    >>> # Add the document to an index
    >>> index = client.get_index('existing-index-id')
    >>> index.add_document(document)

Fields
~~~~~~

Fields belong to documents and are the data that actually gets searched.
Each field can have multiple values,
and there are three different types of tokenization for string values:

- **Atom** (``atom``) means "don't tokenize this string", treat it as one thing
  to compare against.
- **Text** (``text``) means "treat this string as normal text" and split words
  apart to be compared against.
- **HTML** (``html``) means "treat this string as HTML", understanding the
  tags, and treating the rest of the content like Text.

You can set this using the ``tokenization`` paramater when adding a field
value::

    >>> from gcloud import search
    >>> document = search.Document('document-id')
    >>> document.add_field(search.Field('field-name', values=[
    ...     search.Value('britney spears', tokenization='atom'),
    ...     search.Value('<h1>Britney Spears</h1>', tokenization='html'),
    ...     ]))

Searching
~~~~~~~~~

Once you have indexes full of documents, you can search through them by
issuing a search query.

Here's a simple example of how you might start searching::

    >>> from gcloud import search
    >>> client = search.Client()

    >>> index = client.get_index('existing-index-id')
    >>> query = search.Query('britney spears')
    >>> matching_documents = index.search(query)
    >>> for document in matching_documents:
    ...     print document

By default, all queries are sorted by the ``rank`` value you set
when the documented was created.
If you want to sort differently, use the ``order_by`` parameter::

    >>> from gcloud import search
    >>> query = search.Query('britney spears', order_by=['field1', '-field2'])

Note that the ``-`` character before ``field2`` means that
this query will be sorted ascending by ``field1``
and then descending by ``field2``.

If you want only want certain fields to be returned in the match,
you can use the ``fields`` paramater::

    >>> from gcloud import search
    >>> query = search.Query('britney spears', fields=['field1', 'field2'])

