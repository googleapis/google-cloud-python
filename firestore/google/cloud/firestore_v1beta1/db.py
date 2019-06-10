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
    * :class:`~.firestore_v1beta1.client.db.FloatingPointNumberField`
    * :class:`~.firestore_v1beta1.client.db.BytesField`
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
from datetime import datetime, date


class _Field(object):
    def __init__(self, field_type, default=None, required=False):
        if type(self) is _Field:
            raise Exception("You must extend _Field")
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

        if not isinstance(value, self.type) and value is not None:
            raise InvalidValueError(self, value)
        return value


class FirestoreModel(object):
    """Creates a firestore document under the collection [YourModel]

    Args:
        __parent__ Optional(FirestoreModel.__class__): If this is a sub-collection of another model,
            give an instance of the parent
        **data (kwargs): Values for fields in the new record, e.g User(name="Bob")

    Attributes:
        id (str or int): Unique id identifying this record,
            if auto-generated, this is not available before `put()`

        __sub_collection__ (str of FirestoreModel)(Optional class attribute):
                1: A :class:`~.firestore_v1beta1.client.db.FirestoreModel` class where each document in this
                    model is a subcollection of a record in the returned
                    :class:`~.firestore_v1beta1.client.db.FirestoreModel`. e.g If you have a `User` model and each `User`
                    has a collection of `Notes`. The model `Notes` would return `User`
                2: A path representing a collection if you don't want your Model to be on the root of the current
                    database, e.g In a shared database: `sales`

        __database_props__ Tuple(Project, Credentials, database): A tuple of `Project`, `Credentials` and `database` in
            that order
            provide these values if you are not working on App Engine environment or any other case where you need to
            the `Project`, `Credentials` and the `database` that the model is going to use
    """

    __database_props__ = (None, None, DEFAULT_DATABASE)
    __sub_collection__ = None

    def __init__(self, __parent__=None, **data):
        if type(self) is FirestoreModel:
            raise Exception("You must extend FirestoreModel")
        self.__setup_fields()
        self.__model_name = type(self).__name__
        client = self.__init_client()
        self.__collection = client.collection(self.__collection_path(__parent__))
        self.id = None
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            if key in self.__fields:
                setattr(self, key, value)
            else:
                raise InvalidPropertyError(key, self.__model_name)

    @classmethod
    def __collection_path(cls, __parent__):
        sub_collection = cls.__sub_collection__
        if not sub_collection:
            if __parent__:
                raise Exception("__parent__ provided in a model that doesn't provide a subcollection")
            return cls.__name__
        if isinstance(sub_collection, str):  # In this case the subcollection is just a path
            return sub_collection + "/" + cls.__name__
        if not issubclass(sub_collection, FirestoreModel):
            raise SubCollectionError("`__sub_collection__` must return a subclass of `FirestoreModel`")
        if not __parent__:  # We need to have a parent model to compare the subclass to
            raise SubCollectionError("Variable `__parent__` is required to initialize a sub-collection")
        # We expect the parent to be an instance of the model returned
        if not isinstance(__parent__, sub_collection):
            raise SubCollectionError("The __parent__ of a subcollection must be of the same instance as "
                                     "the return of `__sub_collection__`")
        return __parent__._reference_path() + "/" + cls.__name__

    def __document__(self):
        if not self.id:
            return None
        # Get's the absolute path: `projects/{project_id}/databases/{database_id}/documents/{document_path}
        return self.__collection.document(self.id)

    def _reference_path(self):
        if not self.id:
            return None
        # Get's the reference relative to the database
        return self.__collection.document(self.id).path()

    @classmethod
    def __init_client(cls):
        project, credentials, database = cls.__database_props__
        return Client(project=project, credentials=credentials, database=database)

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
                if isinstance(value, ReferenceField):
                    sub_c = value.model.__sub_collection__
                    if sub_c and issubclass(sub_c, FirestoreModel):
                        if not self.__sub_collection__:
                            raise ReferenceFieldError("Reference fields must belong to the same parent as the model, "
                                                      "they therefore must have the same __sub_collection__, %s"
                                                      "does not define a __sub_collection__" % type(self).__name__)
                        if self.__sub_collection__ != sub_c:
                            raise ReferenceFieldError("Reference fields must belong to the same parent as the model, "
                                                      "they therefore must have the same __sub_collection__")

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
            return
        _time, new_ref = self.__collection.add(data)
        self.id = new_ref.id

    def delete(self):
        """Delete the document connected to this model from firestore"""
        if self.id:
            self.__collection.document(self.id).delete()
        self.__del__()

    @classmethod
    def get(cls, id, __parent__=None):
        """
        Get a model with the given id

        Args:
            id (str or int): A key or id of the model record, when a list is provided, `get` returns a list
                models
            __parent__ (FirestoreModel): If querying a sub collection of model, provide the parent instance

        Returns:
            FirestoreModel: An instance of the firestore model calling get
            None: If the id provided doesn't exist
        """
        document = cls.__init_client().collection(cls.__collection_path(__parent__)).document(id)
        data = document.get()
        if not data.exists:
            return None
        return cls(__parent__=__parent__, id=id, **data.to_dict())

    @classmethod
    def query(cls, offset=0, limit=0, __parent__=None):
        """
        Create a query to this model

        Args:
            offset (int): The position in the database where the results begin
            limit (int): Maximum number of records to return
            __parent__ (FirestoreModel): If querying a sub collection of model, provide the parent instance

        Returns:
            An iterable query object
        """
        path = cls.__collection_path(__parent__)
        collection = cls.__init_client().collection(path)
        return Query(cls, offset, limit, collection, __parent__)


class Query(object):
    """
    A  query object is returned when you call :class:`~.firestore_v1beta1.client.db.FirestoreModel`.query().
    You can iterate over the query to get the results of your query one by one. Each item is an instance of a
    :class:`~.firestore_v1beta1.client.db.FirestoreModel`
    """

    def __init__(self, model, offset, limit, collection, parent):
        self.__query = collection
        self.parent = parent
        if offset:
            self.__query = self.__query.offset(offset)
        if limit:
            self.__query = self.__query.limit(limit)
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

    def equal(self, field, value):
        """
        A query condition where field == value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__query = self.__query.filter(field, "==", self.__validate_value(field, value))
        return self

    def greater_than(self, field, value):
        """
        A query condition where field > value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.filter(field, ">", self.__validate_value(field, value))

    def less_than(self, field, value):
        """
        A query condition where field < value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.filter(field, "<", self.__validate_value(field, value))

    def greater_than_or_equal(self, field, value):
        """
        A query condition where field >= value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.filter(field, ">=", self.__validate_value(field, value))

    def less_than_or_equal(self, field, value):
        """
        A query condition where field <= value

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

        Returns:
            Query: A query object with this condition added
        """
        self.__add_range_filter(field)
        self.__query = self.__query.filter(field, "<=", self.__validate_value(field, value))

    def contains(self, field, value):
        """
        A query condition where `value in field`

        Args:
             field (str): The name of a field to compare
             value (Any): The value to compare from the field

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
        self.__query = self.__query.filter(field, "array_contains", value)
        return self

    def order_by(self, field, direction="ASC"):
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
        self.__query = self.__query.order_by(field, direction=direction)
        return self

    def __fetch(self):
        self.__docs = self.__query.stream()
        self.__fetched = True

    def __iter__(self):
        return self

    def fetch(self):
        """
        Get the results of the query as a list

        Returns:
            list (FirestoreModel): A list of models for the found results
        """
        return [model for model in self]

    def __next__(self):
        # Fetch data from db if not already done
        if not self.__fetched:
            self.__fetch()
        doc = self.__docs.__next__()
        return self.__model(__parent__=self.parent, id=doc.id, **doc.to_dict())


class StringField(_Field):
    """
    A string field
    """
    def __init__(self, default=None, length=None, required=False):
        super(StringField, self).__init__(str, default=default, required=required)
        self.length = length

    def validate(self, value):
        value = super(StringField, self).validate(value)
        if self.length and value is not None and len(value) > self.length:
            raise InvalidValueError(self, value)
        return value


class IntegerField(_Field):
    """This field stores a 64-bit signed integer"""
    def __init__(self, default=None, required=False):
        super(IntegerField, self).__init__(int, default=default, required=required)


class FloatingPointNumberField(_Field):
    """Stores a 64-bit double precision floating number"""
    def __init__(self, default=None, required=False):
        super(FloatingPointNumberField, self).__init__((float, int), default=default, required=required)


class BytesField(_Field):
    """Stores values as bytes, can be used to save a blob"""
    def __init__(self, default=None, required=False):
        super(BytesField, self).__init__(bytes, default=default, required=required)


class ListField(_Field, list):
    """A List field"""
    def __init__(self, field_type):
        super(ListField, self).__init__(list, default=[])
        self.field_type = field_type

    def validate(self, value):
        value = super(ListField, self).validate(value)
        for item in value:
            self.field_type.validate(item)
        return value


class ReferenceField(_Field):
    """
    A field referencing/pointing to another model.

    Args:
        model (FirestoreModel.__type__): The model at which this field will be referencing
            NOTE:
                A referenced model must meet one of the following:
                    1. In the same subcollection as the current model
                    2. In a static subcollection defined by a string path
                    3. At the to level of the database
        required (bool): Enforce that this model not store empty data
    """
    def __init__(self, model, required=False):
        if not issubclass(model, FirestoreModel):
            raise ReferenceFieldError()
        super(ReferenceField, self).__init__(model, required=required)
        self.model = model

    def validate(self, value):
        value = super(ReferenceField, self).validate(value)
        if not value:
            return
        return value.__document__()


class DictField(_Field):
    """
    Holds an Dictionary of JSON serializable field data usually

    The value of this field can be a dict or a valid json string. The string will be converted to a dict
    """
    def __init__(self, required=False, default=None):
        super(DictField, self).__init__(dict, required=required, default=default)

    def validate(self, value):
        # Accept valid JSON as a value
        if isinstance(value, str) and value:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise InvalidValueError(self, value)
        value = super(DictField, self).validate(value)
        if not value:
            return value
        # This will raise any errors if the data is not convertible to valid JSON
        try:
            json.dumps(value)
        except TypeError:
            raise InvalidValueError(self, value)
        return value


class BooleanField(_Field):
    """A boolean field, holds True or False"""
    def __init__(self, default=None, required=False):
        super(BooleanField, self).__init__(bool, default=default, required=required)


class DateTimeField(_Field):
    """
    Holds a date time value, if `auto_now` is true the value you set will be overwritten with the current server value

    Args:
        default (datetime)
        required (bool): Enforce that this field can't be submitted when empty
        auto_now (bool): Set to the current time every time the model is updated
        auto_add_now (bool): Set to the current time when a record is created
    """
    def __init__(self, default=None, required=False, auto_now=False, auto_add_now=False):
        if not default and auto_add_now:
            default = SERVER_TIMESTAMP
        super(DateTimeField, self).__init__((datetime, date), default=default, required=required)
        self.auto_now = auto_now

    def validate(self, value):
        # Return server timestamp as the value
        if value == SERVER_TIMESTAMP or self.auto_now:
            return SERVER_TIMESTAMP
        if value is None and self.default == SERVER_TIMESTAMP:
            return SERVER_TIMESTAMP
        return super(DateTimeField, self).validate(value)


class InvalidValueError(ValueError):
    """Raised if the value of a field does not fit the field type"""
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return "%s is not a valid value for field %s of type %s" %\
            (self.value, self.field.name, type(self.field).__name__)


class MalformedQueryError(Exception):
    """Raised when the rules of a query are broken"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidPropertyError(Exception):
    """Raised if a non-existent field is provided during the creation of a model"""
    def __init__(self, prop_name, model_name):
        self.prop_name = prop_name
        self.model_name = model_name

    def __str__(self):
        return "%s not found in model %s" % (self.prop_name, self.model_name)


class SubCollectionError(Exception):
    """Raised when conditions of a subcollection are not met"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ReferenceFieldError(Exception):
    """Raised when a reference field point's to a location the model can't resolve"""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
