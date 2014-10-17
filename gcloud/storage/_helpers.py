"""Helper functions for Cloud Storage utility classes.

These are *not* part of the API.
"""


class _MetadataMixin(object):
    """Abstract mixin for cloud storage classes with associated metadata.

    Expected to be subclasses by :class:`gcloud.storage.bucket.Bucket`
    and :class:`gcloud.storage.key.Key` and both of those classes
    will implemented the abstract parts:
      - LOAD_FULL_FIELDS
      - ACL_CLASS
      - ACL_KEYWORD
      - connection
      - path
    """

    LOAD_FULL_FIELDS = None
    """Tuple of fields which pertain to metadata.

    Expected to be set by subclasses. Fields in this tuple will cause
    `get_metadata()` to do a full reload of all metadata before
    returning.
    """

    ACL_CLASS = type(None)
    """Class which holds ACL data for a given type.

    Expected to be set by subclasses.
    """

    ACL_KEYWORD = None
    """Keyword for ACL_CLASS constructor to pass an object in.

    Expected to be set by subclasses.
    """

    def __init__(self):
        # These should be set by the superclass.
        self.metadata = None
        self.acl = None

    @property
    def connection(self):
        """Abstract getter for the connection to use."""
        raise NotImplementedError

    @property
    def path(self):
        """Abstract getter for the object path."""
        raise NotImplementedError

    def has_metadata(self, field=None):
        """Check if metadata is available.

        :type field: string
        :param field: (optional) the particular field to check for.

        :rtype: bool
        :returns: Whether metadata is available locally.
        """
        if not self.metadata:
            return False
        elif field and field not in self.metadata:
            return False
        else:
            return True

    def reload_metadata(self, full=False):
        """Reload metadata.

        :type full: bool
        :param full: If True, loads all data (include ACL data).

        :rtype: :class:`_MetadataMixin`
        :returns: The object you just reloaded data for.
        """

        projection = 'full' if full else 'noAcl'
        query_params = {'projection': projection}
        self.metadata = self.connection.api_request(
            method='GET', path=self.path, query_params=query_params)
        return self

    def get_metadata(self, field=None, default=None):
        """Get all metadata or a specific field.

        If you request a field that isn't available,
        and that field can be retrieved by refreshing data,
        this method will reload the data using
        :func:`_MetadataMixin.reload_metadata`.

        :type field: string
        :param field: (optional) A particular field to retrieve from metadata.

        :type default: anything
        :param default: The value to return if the field provided wasn't found.

        :rtype: dict or anything
        :returns: All metadata or the value of the specific field.
        """

        if not self.has_metadata(field=field):
            full = (field and field in self.LOAD_FULL_FIELDS)
            self.reload_metadata(full=full)

        if field:
            return self.metadata.get(field, default)
        else:
            return self.metadata

    def patch_metadata(self, metadata):
        """Update particular fields of this object's metadata.

        This method will only update the fields provided
        and will not touch the other fields.

        It will also reload the metadata locally
        based on the servers response.

        :type metadata: dict
        :param metadata: The dictionary of values to update.

        :rtype: :class:`_MetadataMixin`
        :returns: The current object.
        """
        self.metadata = self.connection.api_request(
            method='PATCH', path=self.path, data=metadata,
            query_params={'projection': 'full'})
        return self

    def reload_acl(self):
        """Reload the ACL data.

        :rtype: :class:`_MetadataMixin`
        :returns: The current object.
        """
        self.acl = self.ACL_CLASS(**{self.ACL_KEYWORD: self})

        for entry in self.get_metadata('acl', []):
            entity = self.acl.entity_from_dict(entry)
            self.acl.add_entity(entity)

        return self

    def get_acl(self):
        """Get ACL metadata as an object of type `ACL_CLASS`.

        :returns: An ACL object for the current object.
        """
        if not self.acl:
            self.reload_acl()
        return self.acl

    def save_acl(self, acl=None):
        """Save the ACL data for this object.

        If called without arguments, this will save the ACL currently
        stored on the current object.

        For example, for a `metadata_object` this will save the ACL
        stored in ``some_other_acl``::

           >>> metadata_object.acl = some_other_acl
           >>> metadata_object.save_acl()

        You can also provide a specific ACL to save instead of the one
        currently set on the object::

           >>> metadata_object.save_acl(acl=my_other_acl)

        You can use this to set access controls to be consistent from
        one object to another::

          >>> metadata_object1 = get_object(object1_name)
          >>> metadata_object2 = get_object(object2_name)
          >>> metadata_object2.save_acl(metadata_object1.get_acl())

        If you want to **clear** the ACL for the object, you must save
        an empty list (``[]``) rather than using ``None`` (which is
        interpreted as wanting to save the current ACL)::

          >>> metadata_object.save_acl(None)  # Saves current ACL (self.acl).
          >>> metadata_object.save_acl([])  # Clears current ACL.

        :param acl: The ACL object to save.
                    If left blank, this will save the ACL
                    set locally on the object.
        """
        # NOTE: If acl is [], it is False-y but the acl can be set to an
        #       empty list, so we only override a null input.
        if acl is None:
            acl = self.acl

        if acl is None:
            return self

        self.patch_metadata({'acl': list(acl)})
        self.reload_acl()
        return self

    def clear_acl(self):
        """Remove all ACL rules from the object.

        Note that this won't actually remove *ALL* the rules, but it
        will remove all the non-default rules. In short, you'll still
        have access to the object that you created even after you
        clear ACL rules with this method.

        For example, imagine that you granted access to a Bucket
        (inheriting from this class) to a bunch of coworkers::

          >>> from gcloud import storage
          >>> connection = storage.get_connection(project, email,
                                                  private_key_path)
          >>> bucket = connection.get_bucket(bucket_name)
          >>> acl = bucket.get_acl()
          >>> acl.user('coworker1@example.org').grant_read()
          >>> acl.user('coworker2@example.org').grant_read()
          >>> acl.save()

        Now they work in another part of the company
        and you want to 'start fresh' on who has access::

          >>> acl.clear_acl()

        At this point all the custom rules you created have been removed.
        """
        return self.save_acl(acl=[])

    def make_public(self):
        """Make this object public giving all users read access.

        :returns: The current object.
        """

        self.get_acl().all().grant_read()
        self.save_acl()
        return self
