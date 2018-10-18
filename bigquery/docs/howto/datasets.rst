Managing Datasets
~~~~~~~~~~~~~~~~~

A dataset represents a collection of tables, and applies several default
policies to tables as they are created:

- An access control list (ACL).  When created, a dataset has an ACL
  which maps to the ACL inherited from its project.

- A default table expiration period.  If set, tables created within the
  dataset will have the value as their expiration period.

See BigQuery documentation for more information on
`Datasets <https://cloud.google.com/bigquery/docs/datasets>`_.


Dataset operations
^^^^^^^^^^^^^^^^^^

List datasets for a project with the
:func:`~google.cloud.bigquery.client.Client.list_datasets` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_list_datasets]
   :end-before: [END bigquery_list_datasets]

Create a new dataset with the
:func:`~google.cloud.bigquery.client.Client.create_dataset` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_create_dataset]
   :end-before: [END bigquery_create_dataset]

Get a dataset resource (to pick up changes made by another client) with the
:func:`~google.cloud.bigquery.client.Client.get_dataset` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_get_dataset]
   :end-before: [END bigquery_get_dataset]

Update a property in a dataset's metadata with the
:func:`~google.cloud.bigquery.client.Client.update_dataset` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_dataset_description]
   :end-before: [END bigquery_update_dataset_description]

Modify user permissions on a dataset with the
:func:`~google.cloud.bigquery.client.Client.update_dataset` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_update_dataset_access]
   :end-before: [END bigquery_update_dataset_access]

Delete a dataset with the
:func:`~google.cloud.bigquery.client.Client.delete_dataset` method:

.. literalinclude:: ../snippets.py
   :language: python
   :dedent: 4
   :start-after: [START bigquery_delete_dataset]
   :end-before: [END bigquery_delete_dataset]
