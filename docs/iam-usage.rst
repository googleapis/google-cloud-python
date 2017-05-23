
  This document assumes basic knowledge of Google IAM,
  see `the docs <https://cloud.google.com/iam/docs/>`_ for details

Google Identity and Access Management (IAM), is a system for managing Access Control Lists (ACLs) on Google Cloud Resources.
It represents a shared interface used accross a growing number of Google Cloud APIs.

IAM Types
-------------

The ``iam`` module provides a number of types and convenience functions for interacting with IAM.

.. note::
  When ``resource`` is used throughout this document, it refers to an object backed by a Google Cloud API which implements the IAM-Meta API.
  e.g:
  >>> from gcloud import pubsub
  >>> client = pubsub.Client()
  >>> resource = client.Topic('my-topic')

Members
~~~~~~~
An IAM member is one of the following:

-  An individual Google account: ``iam.user(email)``, or ``'user:{email}'``.
-  A Google Service Account: ``iam.service_account(email)``, or ``'serviceAccount:{email}'``.
-  A Google Group: ``iam.group(email)``, or ``'group:{email}``.
-  A Google Apps domain: ``iam.domain(domain_name)``, or ``'domain:{email}``.
-  Any authenticated Google user: ``iam.ALL_AUTHENTICATED_USERS``, or ``'allAuthenticatedUsers'``.
-  Anyone: ``iam.ALL_USERS``, or ``'allUsers'``.

.. note::
  All of these are convenience wrappers around strings.
  See the list of member string formats `here <https://cloud.google.com/iam/docs/managing-policies>`_.

Roles
~~~~~

Roles represent bundles of permissions that can be added to members.
For a complete list of roles available on a resource run::

    >>> resource.get_roles()

An ``iam.Role`` object has a name, title, and description

- ``name``: the canonical name of a role. This will be the value
  used as keys in policy dictionaries (see below), and will be
  referred to as the "role string" throughout this document.
  E.g. ``'roles/owner'``.
- ``title``: human readable title of the role. E.g. ``'Owner'``
- ``description``: the description of a role.

Policies
~~~~~~~~

A policy consists of three items, which are returned as a tuple by ``resource.get_policy()`` (see below):

- A policy dictionary, where the keys are role strings, and the values are ``set`` s of member strings.
- A version. An integer for end-user bookkeeping.
- An etag used to provide optimistic concurrency controls on policy updates.


Methods
----------------------------------

Resources that implement the IAM interface provide the following methods:

``get_policy`` returns a tuple of ``(policy, version, etag)`` on the corresponding resource.

>>> policy, version, etag = resource.get_policy()
>>> policy
{
   'roles/owner': set(['user:alice@example.com']),
   'roles/editor: set(['group:admins@example.com']),
   'roles/reader': set(['domain:example.com', 'user:bob@example.com'])

- A policy dictionary, where the keys are role strings, and the values are ``set`` s of member strings.
- A version. An integer for end-user bookkeeping.
- An etag used to provide optimistic concurrency controls on policy updates.


Methods
----------------------------------

Resources that implement the IAM interface provide the following methods:

``get_policy`` returns a tuple of ``(policy, version, etag)`` on the corresponding resource.

>>> policy, version, etag = resource.get_policy()
>>> policy
{
   'roles/owner': set(['user:alice@example.com']),
   'roles/editor: set(['group:admins@example.com']),
   'roles/reader': set(['domain:example.com', 'user:bob@example.com'])
}
>>> version
0
>>> etag
ffdFADFdsgfsjrsHTY

``set_policy`` takes one positional, and three keyword arguments:

- The first argument is a policy dictionary, described above.
- ``version`` is an optional integer. If ommited the version of the policy will be set to 0
- ``etag`` is used to set concurreny control. If updates are made to your policy during this change, they will be overwritten with exactly what is in your policy, or, if an etag is specified they will fail with a ``iam.ConcurrentModificationError``
- ``client`` is optionally, a client to make the request with. It will default to the client set on ``resource``


Methods
----------------------------------

Resources that implement the IAM interface provide the following methods:

``get_policy`` returns a tuple of ``(policy, version, etag)`` on the corresponding resource.

>>> policy, version, etag = resource.get_policy()
>>> policy
{
   'roles/owner': set(['user:alice@example.com']),
   'roles/editor: set(['group:admins@example.com']),
   'roles/reader': set(['domain:example.com', 'user:bob@example.com'])
}
>>> version
0
>>> etag
ffdFADFdsgfsjrsHTY

``set_policy`` takes one positional, and three keyword arguments:

- The first argument is a policy dictionary, described above.
- ``version`` is an optional integer. If ommited the version of the policy will be set to 0
- ``etag`` is used to set concurreny control. If updates are made to your policy during this change, they will be overwritten with exactly what is in your policy, or, if an etag is specified they will fail with a ``iam.ConcurrentModificationError``
- ``client`` is optionally, a client to make the request with. It will default to the client set on ``resource``

>>> policy['roles/owner'].add('user:charles@example.com')
>>> policy, version, etag = resource.set_policy(policy, version=version+1, etag=etag)
>>> policy
{
   'roles/owner': set(['user:alice@example.com', 'user:charles@example.com']),
   'roles/editor: set(['group:admins@example.com']),
   'roles/reader': set(['domain:example.com', 'user:bob@example.com'])
}
>>> version
1
>>> etag
ffdFADFdsgfsjrsHTY

``get_roles()`` returns a list of ``iam.Role`` objects that represent roles (and their associated metadata)
which can be granted on the specified resource

>>> resource.get_roles()
[<Role: 'roles/owner'>, <Role: 'roles/editor'>, <Role: 'roles/reader'>]

IAM for Contributors
==========================

To add support for IAM to your resource, the following conditions must be met:

* The class must represent a resource that implements the IAM Meta API.
* The object must provide a ``path`` property (a string that describes the canonical resource path).
* The object must provide a ``self._require_client`` method, which takes an optional ``Client`` object and returns an authenticated ``Client``.

If all of these conditions are met, then IAM support can be added to your class by simply inheriting from ``iam._IAMMixin``
