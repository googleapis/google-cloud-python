"""
A class that inherits from :class:`~.firestore_v1beta1.client.db.FirestoreModel` represents a structure of documents
stored in cloud firestore. Applications define model classes to indicate the structure of their entities,
then instantiate those model classes to create entities. All model classes must inherit (directly or indirectly) from
:class:`~.firestore_v1beta1.client.db.FirestoreModel`.

In a nutshell this library implements:

* a :class:`~.firestore_v1beta1.client.db.FirestoreModel` extendable to build your model
* FieldTypes for use in :class:`~.firestore_v1beta1.client.db.FirestoreModel` including:
    * :class:`~.firestore_v1beta1.client.db.StringField`
    * :class:`~.firestore_v1beta1.client.db.IntegerField`
    * :class:`~.firestore_v1beta1.client.db.ListField`
    * :class:`~.firestore_v1beta1.client.db.ReferenceField`
    * :class:`~.firestore_v1beta1.client.db.JSONField`
    * :class:`~.firestore_v1beta1.client.db.BooleanField`
    * :class:`~.firestore_v1beta1.client.db.DateTimeField`
"""

from google.cloud.firestore_v1beta1.client import Client, DEFAULT_DATABASE
from google.cloud.firestore_v1beta1.query import Query as FSQuery
from google.cloud.firestore_v1beta1 import SERVER_TIMESTAMP
import json
from datetime import datetime
from typing import Type


class _Field(object):
    def __init__(self, field_type, default=None, required=False):
        self.type = field_type
        self.default = default
        self.required = required
        self.name = None

    def validate(self, value):
        if self.required and self.default is None and value is None:
            raise InvalidValueError(self, value)
        # Assign a default value if None is provided
        if value is None:
            value = self.default
        if isinstance(value, self.type) or value is None:
            raise InvalidValueError(self, value)
        return value


class FirestoreModel(object):
    """Creates a firestore document under the collection [YourModel]

    Args:
        __parent__ Optional(Type[FirestoreModel]): If this is a sub-collection of another model,
            give an instance of the parent
        **data (kwargs): Values for fields in the new record, e.g User(name="Bob")

    Attributes:
        id (str or int): Unique id identifying this record, if auto-generated, this is not available before `put()`
    """
    def __init__(self, __parent__: Type['FirestoreModel'] = None, **data):
        path_prefix = self.__collection_prefix(__parent__)
        self.__setup_fields()
        self.__model_name = type(self).__name__
        client = self.__init_client__()
        self.__collection = client.collection("%s/%s" % (path_prefix, self.__model_name))
        self.id = None
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            if key in self.__fields:
                setattr(self, key, value)
            else:
                raise InvalidPropertyError(key, self.__model_name)

    def __collection_prefix(self, __parent__):
        try:
            sub_collection = self.__sub_collection__()
            if isinstance(sub_collection, str):  # In this case the subcollection is just a path
                return sub_collection
            if not issubclass(sub_collection, FirestoreModel):
                raise SubCollectionError("`__sub_collection__` must return a subclass of `FirestoreModel`")
            if not __parent__:  # We need to have a parent model to compare the subclass to
                raise SubCollectionError("Variable `__parent__` is required to initialize a sub-collection")
            # We expect the parent to be an instance of the model returned
            if not isinstance(__parent__, sub_collection):
                raise SubCollectionError("The __parent__ of a subcollection must be of the same instance as "
                                         "the return of `__sub_collection__`")
            return __parent__._reference_path()
        except NotImplementedError:
            if __parent__:
                raise Exception("__parent__ provided in a model that doesn't provide a subcollection")
            return ""

    def _document_path(self):
        if not self.id:
            return None
        # Get's the absolute path: `projects/{project_id}/databases/{database_id}/documents/{document_path}
        return self.__collection.document(self.id)._document_path()

    def _reference_path(self):
        if not self.id:
            return None
        # Get's the reference relative to the database
        return self.__collection.document(self.id).path()

    @classmethod
    def __init_client__(cls):
        try:
            project, credentials, database = cls.__database_props__()
        except NotImplementedError:
            project, credentials, database = (None, None, DEFAULT_DATABASE)
        return Client(project=project, credentials=credentials, database=database)

    @classmethod
    def __database_props__(cls):
        """
        Override this method if you are not working on App Engine environment or any other case where you need to
        the `Project`, `Credentials` and the `database` that the model is going to use

        .. note::
            This is a classmethod and therefore should be overridden as such, i.e. must be decorated with `@classmethod`

        Returns:
            (Project, Credentials, database): A tuple of `Project`, `Credentials` and `database` in that order

        Raises:
            NotImplementedError: Raised if this method is not overridden, You don't need to override this method if
                you're already in an authorized environment e.g. App Engine or Firebase Admin
        """
        raise NotImplementedError()

    @classmethod
    def __sub_collection__(cls):
        """
        Override this method this is a sub collection of another model, or just a constant path

        .. note::
            This is a classmethod and therefore should be overridden as such, i.e. must be decorated with `@classmethod`

        Returns:
            String: A path representing a collection if you don't want your Model to be on the root of the current
                database, e.g In a shared database: `sales`

            Type[Firestore]: A :class:`~.firestore_v1beta1.client.db.FirestoreModel` class where each document in this
                model is a subcollection of a record in the returned
                :class:`~.firestore_v1beta1.client.db.FirestoreModel`. e.g If you have a `User` model and each `User`
                has a collection of `Notes`. The model `Notes` would return `User`

        Raises:
            NotImplementedError: Raised if this method is not overridden. You don't need to implement this method if
                your model is not a subcollection
        """
        raise NotImplementedError()

    def __str__(self):
        return "<FirestoreModel %s>" % self.__model_name

    def __setup_fields(self):
        # Get defined fields, equate them to their defaults
        self.__fields = dict()
        for attribute in dir(self):
            if attribute.startswith("_"):
                continue
            value = getattr(self, attribute)
            if isinstance(value, _Field):
                value.name = attribute
                self.__fields[attribute] = value
                setattr(self, attribute, value.default)

    def __prepare(self):
        # Find current field values and validate them
        values = dict()
        for key, field in self.__fields.items():
            value = getattr(self, key)
            values[key] = field.validate(value)
        return values

    def put(self):
        """
        Save the models data to Firestore

        Raises:
            InvalidValueError: Raised if the value of a field is invalid, e.g. A required field that's None
        """
        data = self.__prepare()
        if self.id:
            self.__collection.document(self.id).set(data)
        _time, new_ref = self.__collection.add(data)
        self.id = new_ref.id

    @classmethod
    def get(cls, key_id: str or int, parent: Type['FirestoreModel'] = None):
        """
        Get a model with the given/id

        Args:
            key_id (str or int): A key or id of the model record
            parent (Type[FirestoreModel]): If querying a sub collection of model, provide the parent instance

        Returns:
            FirestoreModel: An instance of the firestore model calling get
            
            None: If the id provided doesn't exist
        """
        document = cls.__init_client__().collection(cls.__name__).document(key_id)
        data = document.get()
        if not data.exists:
            return None
        return cls(id=key_id, **data.to_dict())

    @classmethod
    def query(cls, offset=0, limit=0):
        """
        Create a query to this model

        Args:
            offset (int): The position in the database where he results begin
            limit (int): Maximum number of records to return

        Returns:
            An iterable query object
        """
        return Query(cls, offset, limit)


class Query(object):
    """
    Creates a query object for the specified model
    """

    def __init__(self, model, offset, limit):
        self.__collection = FirestoreModel.__init_client__().collection(model.__name__)
        if offset:
            self.__collection.start_at(offset)
        if limit:
            self.__collection.limit(limit)
        self.__cursor = 0
        self.__fetched = False
        self.__model = model
        self.__array_contains_queries = 0
        self.__range_filter_queries = {}

    def __validate_value(self, field_name, value):
        field = getattr(self.__model, field_name)
        return field.validate(value)

    def __add_range_filter(self, field):
        self.__range_filter_queries[field] = True

        # Range filter queries are only allowed on a single field at any given time
        if len(self.__range_filter_queries.keys()) > 1:
            raise MalformedQueryError("Range filter queries i.e (<), (>), (<=) and (>=) "
                                      "can only be performed on a single field in a query")

    def equal(self, field: str, value: any):
        """
        A query condition where field == value

        Args:
             field (str): The name of a field to compare
             value (any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__collection.filter(field, "==", self.__validate_value(field, value))
        return self

    def greater_than(self, field: str, value: any):
        """
        A query condition where field > value

        Args:
             field (str): The name of a field to compare
             value (any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__collection.filter(field, ">", self.__validate_value(field, value))

    def less_than(self, field, value):
        """
        A query condition where field < value

        Args:
             field (str): The name of a field to compare
             value (any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__collection.filter(field, "<", self.__validate_value(field, value))

    def greater_than_or_equal(self, field, value):
        """
        A query condition where field >= value

        Args:
             field (str): The name of a field to compare
             value (any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__collection.filter(field, ">=", self.__validate_value(field, value))

    def less_than_or_equal(self, field, value):
        """
        A query condition where field <= value

        Args:
             field (str): The name of a field to compare
             value (any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__collection.filter(field, "<=", self.__validate_value(field, value))

    def contains(self, field, value):
        """
        A query condition where `value in field`

        Args:
             field (str): The name of a field to compare
             value (any): The value to compare from the field

        Returns:
            Query: A query object with this condition added

        Raises:
            MalformedQueryError: If the field specified is not a ListField, or
               the query has more than one contains condition
        """
        model_field = getattr(self.__model, field)

        # Don't do a contains condition in an invalid field
        if not isinstance(model_field, ListField):
            raise MalformedQueryError("Invalid field %s, query field for contains must be a list" % field)

        # Make sure there's only on `array_contains` condition
        self.__array_contains_queries += 1
        if self.__array_contains_queries > 1:
            raise MalformedQueryError("Only one `contains` clause is allowed per query")
        self.__collection.filter(field, "array_contains", value)
        return self

    def order_by(self, field: str, direction: str = "ASC"):
        """
        Set an order for the query, accepts

        Args:
            field (str): The field name to order by
            direction (str: "ASC" or "DESC"), optional:

        Returns:
             Query: A query object with order applied
        """
        if direction is not "ASC" and direction is not "DESC":
            raise MalformedQueryError("order_by direction can only be ASC, or DESC")
        direction = FSQuery.ASCENDING if direction is "ASC" else FSQuery.DESCENDING
        self.__collection.order_by(field, direction=direction)
        return self

    def __fetch__(self):
        self.__docs = self.__collection.get()
        self.__fetched = True

    def __iter__(self):
        return self

    def fetch(self):
        """
        Get the results of the query as a list

        Returns:
            list (Type[FirestoreModel]): A list of models for the found results
        """
        return [model for model in self]

    def __next__(self):
        # Fetch data from db if not already done
        if not self.__fetched:
            self.__fetch__()
        # Reset the cursor if one decides to reuse the query
        if self.__cursor == len(self.__docs):
            self.__cursor = 0
            raise StopIteration
        doc = self.__docs[self.__cursor]
        self.__cursor += 1
        return self.__model(id=doc.id, **doc.to_dict())


class StringField(_Field):
    """A string field"""
    def __init__(self, default=None, length=None, required=False):
        super(StringField, self).__init__(str, default=default, required=required)
        self.length = length

    def validate(self, value):
        """
        Validates that the value provided conforms with the given field

        Raises:
             InvalidValueError: If the value doesn't meet the condition of the field
        """
        value = super(StringField, self).validate(value)
        if self.length and value is not None and len(value) > self.length:
            raise InvalidValueError(self, value)
        return value


class IntegerField(_Field):
    """An Integer field"""
    def __init__(self, default=None, required=False):
        super(IntegerField, self).__init__(int, default=default, required=required)


class ListField(_Field):
    """A List field"""
    def __init__(self, field_type: Type[_Field]):
        super(ListField, self).__init__(list, default=[])
        self.field_type = field_type

    def validate(self, value):
        value = super(ListField, self).validate(value)
        for item in value:
            self.field_type.validate(item)
        return value


class ReferenceField(_Field):
    """A field referencing another model, It's value is an id of the referenced record"""
    def __init__(self, model: Type[FirestoreModel], required=False):
        super(ReferenceField, self).__init__(model, required=required)
        self.model = model

    def validate(self, value):
        value = super(ReferenceField, self).validate(value)
        if not value:
            return
        return self.model.__database_path__


class JSONField(_Field):
    """Holds a dictionary of JSON serializable field data"""
    def __init__(self, required=False, default=None):
        super(JSONField, self).__init__(dict, required=required, default=default)

    def validate(self, value):
        value = super(JSONField, self).validate(value)
        if not value:
            return value
        # This will raise any errors if the data is not convertible to valid JSON
        json.dumps(value)
        return value


class BooleanField(_Field):
    """A boolean field, holds True or False"""
    def __init__(self, default=None, required=False):
        super(BooleanField, self).__init__(bool, default=default, required=required)


class DateTimeField(_Field):
    """Holds a date time value"""
    def __init__(self, default=None, required=False):
        super(DateTimeField, self).__init__(datetime, default=default, required=required)

    def validate(self, value):
        # Return server timestamp as the value
        if value == SERVER_TIMESTAMP:
            return value
        return super(DateTimeField, self).validate(value)


class InvalidValueError(ValueError):
    """Raised if the value of a field does not fit the field type"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return "InvalidValueError %s is not a valid value for field %s of type %s" %\
            (self.value, self.field.name, self.field.type)


class MalformedQueryError(Exception):
    """Raised when the rules of a query are broken"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "MalformedQueryError %s" % self.message


class InvalidPropertyError(Exception):
    """Raised if a non-existent field is provided during the creation of a model"""
    def __init__(self, prop_name, model_name):
        self.prop_name = prop_name
        self.model_name = model_name

    def __str__(self):
        return "InvalidPropertyError: %s not found in model %s" % (self.prop_name, self.model_name)


class SubCollectionError(Exception):
    """Raised when conditions of a subcollection are not met"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "SubCollectionError: %s" % self.message
