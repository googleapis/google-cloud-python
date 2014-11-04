"""Helper functions for Cloud Storage utility classes.

These are *not* part of the API.
"""


class _MetadataMixin(object):
    """Abstract mixin for cloud storage classes with associated metadata.

    Non-abstract subclasses should implement:
      - CUSTOM_METADATA_FIELDS
      - connection
      - path
    """

    CUSTOM_METADATA_FIELDS = None
    """Mapping of field name -> accessor for fields w/ custom accessors.

    Expected to be set by subclasses. Fields in this mapping will cause
    `get_metadata()` to raise a KeyError with a message to use the relevant
    accessor methods.
    """

    def __init__(self, name=None, metadata=None):
        """_MetadataMixin constructor.

        :type name: string
        :param name: The name of the object.

        :type metadata: dict
        :param metadata: All the other data provided by Cloud Storage.
        """
        self.name = name
        self.metadata = metadata

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

    def reload_metadata(self):
        """Reload metadata from Cloud Storage.

        :rtype: :class:`_MetadataMixin`
        :returns: The object you just reloaded data for.
        """
        # Pass only '?projection=noAcl' here because 'acl' and related
        # are handled via 'get_acl()' etc.
        query_params = {'projection': 'noAcl'}
        self.metadata = self.connection.api_request(
            method='GET', path=self.path, query_params=query_params)
        return self

    def get_metadata(self, field=None, default=None):
        """Get all metadata or a specific field.

        If you request a field that isn't available, and that field can
        be retrieved by refreshing data from Cloud Storage, this method
        will reload the data using :func:`_MetadataMixin.reload_metadata`.

        :type field: string
        :param field: (optional) A particular field to retrieve from metadata.

        :type default: anything
        :param default: The value to return if the field provided wasn't found.

        :rtype: dict or anything
        :returns: All metadata or the value of the specific field.

        :raises: :class:`KeyError` if the field is in CUSTOM_METADATA_FIELDS.
        """
        # We ignore 'acl' and related fields because they are meant to be
        # handled via 'get_acl()' and related methods.
        custom = self.CUSTOM_METADATA_FIELDS.get(field)
        if custom is not None:
            message = 'Use %s or related methods instead.' % custom
            raise KeyError((field, message))

        if not self.has_metadata(field=field):
            self.reload_metadata()

        if field:
            return self.metadata.get(field, default)
        else:
            return self.metadata

    def patch_metadata(self, metadata):
        """Update particular fields of this object's metadata.

        This method will only update the fields provided and will not
        touch the other fields.

        It will also reload the metadata locally based on the server's
        response.

        :type metadata: dict
        :param metadata: The dictionary of values to update.

        :rtype: :class:`_MetadataMixin`
        :returns: The current object.
        """
        self.metadata = self.connection.api_request(
            method='PATCH', path=self.path, data=metadata,
            query_params={'projection': 'full'})
        return self

    def get_acl(self):
        """Get ACL metadata as an object.

        :returns: An ACL object for the current object.
        """
        if not self.acl.loaded:
            self.acl.reload()
        return self.acl
