from google.cloud.firestore_v1beta1.client import Client, DEFAULT_DATABASE
from google.cloud.firestore_v1beta1.query import Query
import os
import json
from datetime import datetime, date


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


def initialize_database(project=None, credentials=None, database=DEFAULT_DATABASE):
    """
    Set the parameters to be used when connecting to firestore

    Args:
        project (str): The project this model belongs to
        credentials (str): Path to a credentials file
        database (str): The name of the database to use
    """
    os.environ["__project"] = project
    os.environ["__credentials"] = credentials
    os.environ["__database"] = database


class FirestoreModel(object):
    """
    An equivalent of a top-level firestore collection

    Attributes:
        id (str or int): Unique id identifying this record, if auto-generated, this is not available before `put()`
    """
    def __init__(self, **data):
        """
        Creates a firestore document under the collection __model_name

        Args:
            **data (kwargs): Values for fields in the new record, e.g User(name="Bob")
        """
        self.__setup_fields()
        self.__model_name = type(self).__name__
        client = FirestoreModel.__init_client__()
        self.__collection = client.collection(self.__model_name)
        self.id = None
        self.__db_path__ = client._database_string_internal
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            if key in self.__fields:
                if isinstance(self.__fields[key], DateTimeField) and str(value).isnumeric():
                    value = datetime.fromtimestamp(value)
                setattr(self, key, value)
            else:
                raise InvalidPropertyError(key, self.__model_name)

    @staticmethod
    def __init_client__():
        # These values are stored in ENV in db.initialize_database()
        project = os.environ.get("__project", None)
        credentials = os.environ.get("__credentials", None)
        database = os.environ.get("__database", DEFAULT_DATABASE)
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
    def get(cls, key_id: str or int):
        """
        Get a model with the given/id

        Args:
            key_id (str or int): A key or id of the model record

        Returns:
            FirestoreModel: An instance of the firestore model calling get
            
            None: If the id provided doesn't exist
        """
        document = FirestoreModel.__init_client__().collection(cls.__name__).document(key_id)
        data = document.get()
        if not data.exists:
            return None
        return cls(id=key_id, **data.to_dict())

    class __Query(object):
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
                FirestoreModel.__Query: A query object with this condition added
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
                FirestoreModel.__Query: A query object with this condition added
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
                FirestoreModel.__Query: A query object with this condition added
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
                FirestoreModel.__Query: A query object with this condition added
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
                FirestoreModel.__Query: A query object with this condition added
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
                FirestoreModel.__Query: A query object with this condition added
                 
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
                 FirestoreModel.__Query: A query object with order applied
            """
            if direction is not "ASC" and direction is not "DESC":
                raise MalformedQueryError("order_by direction can only be ASC, or DESC")
            direction = Query.ASCENDING if direction is "ASC" else Query.DESCENDING
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
                list (FirestoreModel): A list of models for the found results
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
        return FirestoreModel.__Query(cls, offset, limit)


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
    def __init__(self, field_type: _Field.__bases__):
        super(ListField, self).__init__(list, default=[])
        self.field_type = field_type

    def validate(self, value):
        value = super(ListField, self).validate(value)
        for item in value:
            self.field_type.validate(item)
        return value


class ReferenceField(_Field):
    """A field referencing another model, It's value is an id of the referenced record"""
    def __init__(self, model: FirestoreModel.__bases__, required=False):
        super(ReferenceField, self).__init__(model, required=required)
        self.model = model

    def validate(self, value):
        value = super(ReferenceField, self).validate(value)
        if not value:
            return
        return "projects/[PROJECT_ID]/databases/[DATABASE_ID]/documents/[DOCUMENT_PATH]"


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


CURRENT_TIMESTAMP = "CURRENT_TIMESTAMP"


class DateTimeField(_Field):
    """Holds a date time value"""
    def __init__(self, default=None, required=False):
        super(DateTimeField, self).__init__(datetime, default=default, required=required)

    def validate(self, value):
        if not self.required and not self.default and value is None:
            return
        # Return current time, we know it's valid
        if self.default is CURRENT_TIMESTAMP:
            return datetime.now().timestamp()

        if not all([isinstance(value, _class) for _class in [datetime, date]]):
            raise InvalidValueError(self, value)

        return value.timestamp()


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
