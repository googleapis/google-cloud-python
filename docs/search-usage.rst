Using the API
=============

Connection / Authorization
--------------------------

Implicitly use the default client:

.. doctest::

  >>> from gcloud import search
  >>> # The search module has the same methods as a client, using the default.
  >>> search.list_indexes()  # API request
  []

Configure the default client:

.. doctest::

  >>> from gcloud import search
  >>> search.set_project_id('project-id')
  >>> search.set_credentials(credentials)
  >>> search.list_indexes()  # API request
  []

Explicitly use the default client:

.. doctest::

  >>> from gcloud.search import default_client as client
  >>> # The default_client is equivalent to search.Client()
  >>> client.list_indexes()  # API request
  []

Explicitly configure a client:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client(project_id='project-id', credentials=credentials)
  >>> client.list_indexes()  # API request
  []

Manage indexes for a project
----------------------------

Create a new index:

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()
   >>> index = client.create_index('index_id')  # API request
   >>> index.id
   'index_id'

Create a new index with a name:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.create_index('index_id', name='Name')  # API request
  >>> index.name
  'Name'

Get or create an index:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_or_create_index('index_id')  # API request
  >>> index.id
  'index_id'

List the indexes:

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()
   >>> [index.id for index in client.list_indexes()]  # API request
   ['index_id']

Retrieve an index:

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()
   >>> index = client.get_index('missing_index_id')  # API request
   >>> index is None
   True
   >>> index = client.get_index('index_id')  # API request
   >>> index.id
   'index_id'

Get an index without making an API request

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id', check=False)
  >>> index.id
  'index_id'

Update an index:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> index.name = 'Name'
  >>> client.update_index(index)

Delete an index by ID:

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()
   >>> client.delete_index('index_id')  # API request

Delete an index:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> index.id
  'index_id'
  >>> client.delete_index(index)  # API request

Manage documents and fields
---------------------------

Create a document

.. doctest::

  >>> from gcloud import search
  >>> document = search.Document('document_id', rank=0)
  >>> document.id
  'document_id'

Add a field to a document

.. doctest::

  >>> from gcloud import search
  >>> document = search.Document('document_id')
  >>> document.add_field(search.Field('fieldname'))

Add values to a field

.. doctest::

  >>> from datetime import datetime
  >>> from gcloud import search
  >>> field = search.Field('fieldname')
  >>> field.add_value('string')
  >>> # Tokenization field ignored for non-string values.
  >>> field.add_value('<h1>string</h1>', tokenization='html')
  >>> field.add_value('string', tokenization='atom')
  >>> field.add_value('string', tokenization='text')
  >>> field.add_value(1234)
  >>> field.add_value(datetime.now())
  >>> len(field.values)
  9

Add values to a field at initialization time

.. doctest::

  >>> from gcloud import search
  >>> field = search.Field('fieldname', values=[
          'string',
          search.Value('<h1>string2</h1>', tokenization='html')
          search.Value('string', tokenization='atom')])

Add a single document to an index:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> document = search.Document('document_id', rank=0)
  >>> index.add_document(document)  # API request

Add multiple documents to an index:

.. doctest::

   >>> from gcloud import search
   >>> client = search.Client()
   >>> index = client.get_index('index_id')  # API request
   >>> documents = [search.Document('document_id')]
   >>> index.add_documents(documents)  # API request

Get a single document by ID:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> document = index.get_document('missing_document_id')  # API request
  >>> document is None
  True
  >>> document = index.get_document('document_id')  # API request
  >>> document.fields
  []

Delete a document by ID:

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> index.delete_document('document_id')  # API request
  >>> index.delete_document('missing_document_id')  # API request

Searching
---------

Create a query

.. doctest::

  >>> from gcloud import search
  >>> query = search.Query('query text here')
  >>> query.query
  'query text here'

Specify the fields to return in a query

.. doctest::

  >>> from gcloud import search
  >>> query = search.Query('query text here', fields=['field1', 'field2'])
  >>> query.fields
  ['field1', 'field2']

Set the sort order of a query

.. doctest::

  >>> from gcloud import search
  >>> query = search.Query('query text here', order_by='field1')
  >>> query.order_by
  'field1'
  >>> query2 = search.Query('query text here', order_by=['field2', 'field3'])
  >>> query2.order_by
  ['field2', 'field3']
  >>> # Order descending by field1 and ascending by field2
  >>> query4 = search.Query('query text here', order_by=['-field1', 'field2'])
  >>> query3.order_by
  ['-field1', 'field2']

Set custom field expressions on a query

.. doctest::

  >>> from gcloud import search
  >>> query = search.Query('query text here')
  >>> query.add_field_expression('total_price', '(price + tax)')
  >>> # We don't do any checks on the expression. These are checked at query time.
  >>> query.add_field_expression('invalid', 'is_prime(num)')
  >>> query.add_field_expression('bad_field', '(missing_field + tax)')

Set custom field expressions at initialization time

.. doctest::

  >>> from gcloud import search
  >>> query = search.Query('query text here', field_expressions={
          'total_price': '(price + tax)'})

Search an index

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> matching = index.search(search.Query('query text here'))  # API request
  >>> for document in matching:
  ...   print document.id

Search an index with a limit on number of results

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> matching = index.search(search.Query('query text here'),
  ...                         limit=42)  # API request

Search an index with a custom page size (advanced)

.. doctest::

  >>> from gcloud import search
  >>> client = search.Client()
  >>> index = client.get_index('index_id')  # API request
  >>> matching = index.search(search.Query('query text here'),
  ...                         page_size=20)  # API request
