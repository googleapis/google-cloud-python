"""Helper functions for Cloud Storage utility classes.

These are *not* part of the API.
"""


class _PropertyMixin(object):
    """Abstract mixin for cloud storage classes with associated propertties.

    Non-abstract subclasses should implement:
      - CUSTOM_PROPERTY_ACCESSORS
      - connection
      - path
    """

    CUSTOM_PROPERTY_ACCESSORS = None
    """Mapping of field name -> accessor for fields w/ custom accessors.

    Expected to be set by subclasses. Fields in this mapping will cause
    :meth:`_get_property()` to raise a KeyError with a message to use the
    relevant accessor methods.
    """

    @property
    def connection(self):
        """Abstract getter for the connection to use."""
        raise NotImplementedError

    @property
    def path(self):
        """Abstract getter for the object path."""
        raise NotImplementedError

    def __init__(self, name=None, properties=None):
        """_PropertyMixin constructor.

        :type name: string
        :param name: The name of the object.

        :type properties: dict
        :param properties: All the other data provided by Cloud Storage.
        """
        self.name = name
        self._properties = {}
        if properties is not None:
            self._properties.update(properties)

    @property
    def properties(self):
        """Ensure properties are loaded, and return a copy.

        :rtype: dict
        """
        if not self._properties:
            self._reload_properties()
        return self._properties.copy()

    def _reload_properties(self):
        """Reload properties from Cloud Storage.

        :rtype: :class:`_PropertyMixin`
        :returns: The object you just reloaded data for.
        """
        # Pass only '?projection=noAcl' here because 'acl' and related
        # are handled via custom endpoints..
        query_params = {'projection': 'noAcl'}
        self._properties = self.connection.api_request(
            method='GET', path=self.path, query_params=query_params)
        return self

    def _patch_properties(self, properties):
        """Update particular fields of this object's properties.

        This method will only update the fields provided and will not
        touch the other fields.

        It will also reload the properties locally based on the server's
        response.

        :type properties: dict
        :param properties: The dictionary of values to update.

        :rtype: :class:`_PropertyMixin`
        :returns: The current object.
        """
        # Pass '?projection=full' here because 'PATCH' documented not
        # to work properly w/ 'noAcl'.
        self._properties = self.connection.api_request(
            method='PATCH', path=self.path, data=properties,
            query_params={'projection': 'full'})
        return self

    def _get_property(self, field, default=None):
        """Return the value of a field from the server-side representation.

        If you request a field that isn't available, and that field can
        be retrieved by refreshing data from Cloud Storage, this method
        will reload the data using :func:`_PropertyMixin._reload_properties`.

        :type field: string
        :param field: A particular field to retrieve from properties.

        :type default: anything
        :param default: The value to return if the field provided wasn't found.

        :rtype: anything
        :returns: value of the specific field, or the default if not found.
        """
        # Raise for fields which have custom accessors.
        custom = self.CUSTOM_PROPERTY_ACCESSORS.get(field)
        if custom is not None:
            message = "Use '%s' or related methods instead." % custom
            raise KeyError((field, message))

        return self.properties.get(field, default)

    def get_acl(self):
        """Get ACL as an object.

        :returns: An ACL object for the current object.
        """
        if not self.acl.loaded:
            self.acl.reload()
        return self.acl
