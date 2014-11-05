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

        :type metadata: dict
        :param metadata: All the other data provided by Cloud Storage.
        """
        self.name = name
        self._properties = {}
        if properties is not None:
            self._properties.update(properties)

    @property
    def properties(self):
        """Ensure properties are loaded, and return a copy.
        """
        if not self._properties:
            self._reload_properties()
        return self._properties.copy()

    metadata = properties  # Backward-compatibiltiy alias

    def _reload_properties(self):
        """Reload properties from Cloud Storage.

        :rtype: :class:`_PropertyMixin`
        :returns: The object you just reloaded data for.
        """
        # Pass only '?projection=noAcl' here because 'acl' and related
        # are handled via 'get_acl()' etc.
        query_params = {'projection': 'noAcl'}
        self._properties = self.connection.api_request(
            method='GET', path=self.path, query_params=query_params)
        return self
    reload_metadata = _reload_properties  # backward-compat alias

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
    patch_metadata = _patch_properties  # backward-compat alias

    def _has_property(self, field=None):
        """Check if property is available.

        :type field: string
        :param field: (optional) the particular field to check for.

        :rtype: boolean
        :returns: Whether property is available locally.  If no ``field``
                  passed, return whether *any* properties are available.
        """
        if field and field not in self._properties:
            return False
        return len(self._properties) > 0
    has_metadata = _has_property  # backward-compat alias

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
            message = 'Use %s or related methods instead.' % custom
            raise KeyError((field, message))

        if not self._properties or field not in self._properties:
            self._reload_properties()

        return self._properties.get(field, default)
    get_metadata = _get_property  # Backward-compat alias

    def get_acl(self):
        """Get ACL as an object.

        :returns: An ACL object for the current object.
        """
        if not self.acl.loaded:
            self.acl.reload()
        return self.acl
