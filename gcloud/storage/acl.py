"""Manipulate access control lists that Cloud Storage provides.

:class:`gcloud.storage.bucket.Bucket` has a getting method that creates
an ACL object under the hood, and you can interact with that using
:func:`gcloud.storage.bucket.Bucket.get_acl`::

  >>> from gcloud import storage
  >>> connection = storage.get_connection(project, email, key_path)
  >>> bucket = connection.get_bucket(bucket_name)
  >>> acl = bucket.get_acl()

Adding and removing permissions can be done with the following methods
(in increasing order of granularity):

- :func:`ACL.all`
  corresponds to access for all users.
- :func:`ACL.all_authenticated` corresponds
  to access for all users that are signed into a Google account.
- :func:`ACL.domain` corresponds to access on a
  per Google Apps domain (ie, ``example.com``).
- :func:`ACL.group` corresponds to access on a
  per group basis (either by ID or e-mail address).
- :func:`ACL.user` corresponds to access on a
  per user basis (either by ID or e-mail address).

And you are able to ``grant`` and ``revoke`` the following roles:

- **Reading**:
  :func:`_ACLEntity.grant_read` and :func:`_ACLEntity.revoke_read`
- **Writing**:
  :func:`_ACLEntity.grant_write` and :func:`_ACLEntity.revoke_write`
- **Owning**:
  :func:`_ACLEntity.grant_owner` and :func:`_ACLEntity.revoke_owner`

You can use any of these like any other factory method (these happen to
be :class:`_ACLEntity` factories)::

  >>> acl.user('me@example.org').grant_read()
  >>> acl.all_authenticated().grant_write()

You can also chain these ``grant_*`` and ``revoke_*`` methods together
for brevity::

  >>> acl.all().grant_read().revoke_write()

After that, you can save any changes you make with the
:func:`gcloud.storage.acl.ACL.save` method::

  >>> acl.save()

You can alternatively save any existing :class:`gcloud.storage.acl.ACL`
object (whether it was created by a factory method or not) with the
:func:`gcloud.storage.bucket.Bucket.save_acl` method::

  >>> bucket.save_acl(acl)

To get the list of ``entity`` and ``role`` for each unique pair, the
:class:`ACL` class is iterable::

  >>> print list(ACL)
  [{'role': 'OWNER', 'entity': 'allUsers'}, ...]

This list of tuples can be used as the ``entity`` and ``role`` fields
when sending metadata for ACLs to the API.
"""


class _ACLEntity(object):
    """Class representing a set of roles for an entity.

    This is a helper class that you likely won't ever construct
    outside of using the factor methods on the :class:`ACL` object.
    """

    READER_ROLE = 'READER'
    WRITER_ROLE = 'WRITER'
    OWNER_ROLE = 'OWNER'

    def __init__(self, entity_type, identifier=None):
        """Entity constructor.

        :type entity_type: string
        :param entity_type: The type of entity (ie, 'group' or 'user').

        :type identifier: string
        :param identifier: The ID or e-mail of the entity. For the special
                           entity types (like 'allUsers') this is optional.
        """
        self.identifier = identifier
        self.roles = set([])
        self.type = entity_type

    def __str__(self):
        if not self.identifier:
            return str(self.type)
        else:
            return '{self.type}-{self.identifier}'.format(self=self)

    def __repr__(self):
        return '<ACL Entity: {self} ({roles})>'.format(
            self=self, roles=', '.join(self.roles))

    def get_roles(self):
        """Get the list of roles permitted by this entity.

        :rtype: list of strings
        :returns: The list of roles associated with this entity.
        """
        return self.roles

    def grant(self, role):
        """Add a role to the entity.

        :type role: string
        :param role: The role to add to the entity.

        :rtype: :class:`_ACLEntity`
        :returns: The entity class.
        """
        self.roles.add(role)
        return self

    def revoke(self, role):
        """Remove a role from the entity.

        :type role: string
        :param role: The role to remove from the entity.

        :rtype: :class:`_ACLEntity`
        :returns: The entity class.
        """
        if role in self.roles:
            self.roles.remove(role)
        return self

    def grant_read(self):
        """Grant read access to the current entity."""

        return self.grant(_ACLEntity.READER_ROLE)

    def grant_write(self):
        """Grant write access to the current entity."""

        return self.grant(_ACLEntity.WRITER_ROLE)

    def grant_owner(self):
        """Grant owner access to the current entity."""

        return self.grant(_ACLEntity.OWNER_ROLE)

    def revoke_read(self):
        """Revoke read access from the current entity."""

        return self.revoke(_ACLEntity.READER_ROLE)

    def revoke_write(self):
        """Revoke write access from the current entity."""

        return self.revoke(_ACLEntity.WRITER_ROLE)

    def revoke_owner(self):
        """Revoke owner access from the current entity."""

        return self.revoke(_ACLEntity.OWNER_ROLE)


class ACL(object):
    """Container class representing a list of access controls."""

    loaded = False

    def __init__(self):
        self.entities = {}

    def clear(self):
        """Remove all entities from the ACL."""
        self.entities.clear()

    def reset(self):
        """Remove all entities from the ACL, and clear the ``loaded`` flag."""
        self.entities.clear()
        self.loaded = False

    def __iter__(self):
        for entity in self.entities.itervalues():
            for role in entity.get_roles():
                if role:
                    yield {'entity': str(entity), 'role': role}

    def entity_from_dict(self, entity_dict):
        """Build an _ACLEntity object from a dictionary of data.

        An entity is a mutable object that represents a list of roles
        belonging to either a user or group or the special types for all
        users and all authenticated users.

        :type entity_dict: dict
        :param entity_dict: Dictionary full of data from an ACL lookup.

        :rtype: :class:`_ACLEntity`
        :returns: An Entity constructed from the dictionary.
        """
        entity = entity_dict['entity']
        role = entity_dict['role']

        if entity == 'allUsers':
            entity = self.all()

        elif entity == 'allAuthenticatedUsers':
            entity = self.all_authenticated()

        elif '-' in entity:
            entity_type, identifier = entity.split('-', 1)
            entity = self.entity(entity_type=entity_type,
                                 identifier=identifier)

        if not isinstance(entity, _ACLEntity):
            raise ValueError('Invalid dictionary: %s' % entity_dict)

        return entity.grant(role)

    def has_entity(self, entity):
        """Returns whether or not this ACL has any entries for an entity.

        :type entity: :class:`_ACLEntity`
        :param entity: The entity to check for existence in this ACL.

        :rtype: bool
        :returns: True of the entity exists in the ACL.
        """
        return str(entity) in self.entities

    def get_entity(self, entity, default=None):
        """Gets an entity object from the ACL.

        :type entity: :class:`_ACLEntity` or string
        :param entity: The entity to get lookup in the ACL.

        :type default: anything
        :param default: This value will be returned if the entity
                        doesn't exist.

        :rtype: :class:`_ACLEntity`
        :returns: The corresponding entity or the value provided
                  to ``default``.
        """
        return self.entities.get(str(entity), default)

    def add_entity(self, entity):
        """Add an entity to the ACL.

        :type entity: :class:`_ACLEntity`
        :param entity: The entity to add to this ACL.
        """
        self.entities[str(entity)] = entity
        self.loaded = True

    def entity(self, entity_type, identifier=None):
        """Factory method for creating an Entity.

        If an entity with the same type and identifier already exists,
        this will return a reference to that entity.  If not, it will
        create a new one and add it to the list of known entities for
        this ACL.

        :type entity_type: string
        :param entity_type: The type of entity to create
                            (ie, ``user``, ``group``, etc)

        :type identifier: string
        :param identifier: The ID of the entity (if applicable).
                           This can be either an ID or an e-mail address.

        :rtype: :class:`_ACLEntity`
        :returns: A new Entity or a reference to an existing identical entity.
        """
        entity = _ACLEntity(entity_type=entity_type, identifier=identifier)
        if self.has_entity(entity):
            entity = self.get_entity(entity)
        else:
            self.add_entity(entity)
        return entity

    def user(self, identifier):
        """Factory method for a user Entity.

        :type identifier: string
        :param identifier: An id or e-mail for this particular user.

        :rtype: :class:`_ACLEntity`
        :returns: An Entity corresponding to this user.
        """
        return self.entity('user', identifier=identifier)

    def group(self, identifier):
        """Factory method for a group Entity.

        :type identifier: string
        :param identifier: An id or e-mail for this particular group.

        :rtype: :class:`_ACLEntity`
        :returns: An Entity corresponding to this group.
        """
        return self.entity('group', identifier=identifier)

    def domain(self, domain):
        """Factory method for a domain Entity.

        :type domain: string
        :param domain: The domain for this entity.

        :rtype: :class:`_ACLEntity`
        :returns: An entity corresponding to this domain.
        """
        return self.entity('domain', identifier=domain)

    def all(self):
        """Factory method for an Entity representing all users.

        :rtype: :class:`_ACLEntity`
        :returns: An entity representing all users.
        """
        return self.entity('allUsers')

    def all_authenticated(self):
        """Factory method for an Entity representing all authenticated users.

        :rtype: :class:`_ACLEntity`
        :returns: An entity representing all authenticated users.
        """
        return self.entity('allAuthenticatedUsers')

    def get_entities(self):
        """Get a list of all Entity objects.

        :rtype: list of :class:`_ACLEntity` objects
        :returns: A list of all Entity objects.
        """
        return self.entities.values()

    def save(self):
        """A method to be overridden by subclasses.

        :raises: NotImplementedError
        """
        raise NotImplementedError


class BucketACL(ACL):
    """An ACL specifically for a bucket."""

    def __init__(self, bucket):
        """
        :type bucket: :class:`gcloud.storage.bucket.Bucket`
        :param bucket: The bucket to which this ACL relates.
        """
        super(BucketACL, self).__init__()
        self.bucket = bucket

    def save(self):
        """Save this ACL for the current bucket."""

        return self.bucket.save_acl(acl=self)


class DefaultObjectACL(BucketACL):
    """A class representing the default object ACL for a bucket."""

    def save(self):
        """Save this ACL as the default object ACL for the current bucket."""

        return self.bucket.save_default_object_acl(acl=self)


class ObjectACL(ACL):
    """An ACL specifically for a key."""

    def __init__(self, key):
        """
        :type key: :class:`gcloud.storage.key.Key`
        :param key: The key that this ACL corresponds to.
        """
        super(ObjectACL, self).__init__()
        self.key = key

    def save(self):
        """Save this ACL for the current key."""

        return self.key.save_acl(acl=self)
