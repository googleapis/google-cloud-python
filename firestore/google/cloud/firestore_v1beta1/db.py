from google.cloud.firestore_v1beta1.client import Client, DEFAULT_DATABASE
import os


class _Field:
    def __init__(self, field_type, default=None, required=False):
        self.type = field_type
        self.default = default
        self.required = required
        self.name = None

    def validate(self, value):
        if self.required and value is None:
            raise InvalidValueError(self, value)
        if isinstance(value, self.type) or value is None:
            raise InvalidValueError(self, value)


def initialize_database(project=None, credentials=None, database=DEFAULT_DATABASE):
    os.environ["__project"] = project
    os.environ["__credentials"] = credentials
    os.environ["__database"] = database


class FirestoreModel:
    def __init__(self, **data):
        """
        :param data:
        """
        self.__setup_fields__()
        self.__db = self.__init_client__()
        self.__model_name = type(self).__name__
        self.__collection = self.__db.collection(self.__model_name)
        self.id = None
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            if key in self.fields:
                setattr(self, key, value)
            else:
                raise InvalidPropertyError(key, self.__model_name)

    @classmethod
    def __init_client__(cls):
        project = os.environ.get("__project", None)
        credentials = os.environ.get("__credentials", None)
        database = os.environ.get("__database", DEFAULT_DATABASE)
        return Client(project=project, credentials=credentials, database=database)

    def __str__(self):
        return "<Model %s>" % self.__model_name

    def __setup_fields__(self):
        self.fields = dict()
        for attribute in dir(self):
            if attribute.startswith("_"):
                continue
            value = getattr(self, attribute)
            if isinstance(value, _Field):
                value.name = attribute
                self.fields[attribute] = value
                setattr(self, attribute, value.default)

    def __prepare__(self):
        values = dict()
        for key, field in self.fields.items():
            value = getattr(self, key)
            field.validate(value)
            values[key] = value
        return values

    def put(self):
        data = self.__prepare__()
        if self.id:
            self.__collection.document(self.id).set(data)
            return True
        _time, new_ref = self.__collection.add(data)
        self.id = new_ref.id
        return True

    @classmethod
    def get(cls, key_id: str):
        db = cls.__init_client__().collection(cls.__name__).document(key_id)
        data = db.get()
        if not data.exists:
            return None
        return cls(id=key_id, **data.to_dict())

    @classmethod
    def query(cls, offset=0, limit=0):
        class Query(object):
            def __init__(self, _offset, _limit):
                self.__collection = cls.__init_client__().collection(cls.__name__)
                if _offset:
                    self.__collection.start_at(_offset)
                if _limit:
                    self.__collection.limit(_limit)
                self.__cursor = 0
                self.__fetched = False
                self.__model = cls

            def equal(self, field, value):
                self.__collection.filter(field, "==", value)
                return self

            def greater_than(self, field, value):
                self.__collection.filter(field, ">", value)

            def less_than(self, field, value):
                self.__collection.filter(field, "<", value)

            def greater_than_or_equal(self, field, value):
                self.__collection.filter(field, ">=", value)

            def less_than_or_equal(self, field, value):
                self.__collection.filter(field, "<=", value)

            def contains(self, field, value):
                model_field = getattr(self.__model, field)
                if not isinstance(model_field, ListField):
                    raise MalformedQueryError("Invalid field %s, query field for contains must be a list" % field)
                self.__collection.filter(field, "array_contains", value)
                return self

            def order_by(self, field):
                self.__collection.order_by(field)
                return self

            def __fetch(self):
                self.__docs = self.__collection.get()
                self.__fetched = True

            def __iter__(self):
                return self

            def fetch(self):
                if not self.__fetched:
                    self.fetch()
                return [model for model in self]

            def __next__(self):
                if not self.__fetched:
                    self.__fetch()

                if self.__cursor == len(self.__docs):
                    self.__cursor = 0
                    raise StopIteration
                doc = self.__docs[self.__cursor]
                self.__cursor += 1
                return self.__model(id=doc.id, **doc.to_dict())

        return Query(cls, offset, limit)


class StringField(_Field):
    def __init__(self, default=None, length=None, required=False):
        super().__init__(str, default=default, required=required)
        self.length = length

    def validate(self, value):
        super().validate(value)
        if self.length and value is not None and len(value) > self.length:
            raise InvalidValueError(self, value)


class IntegerField(_Field):
    def __init__(self, default=None, required=False):
        super().__init__(int, default=default, required=required)


class ListField(_Field):
    def __init__(self, items_field):
        super().__init__(list, default=[])
        self.items_field = items_field

    def validate(self, value):
        self.validate(value)
        for item in value:
            self.items_field.validate(item)


class ReferenceField(_Field):
    def __init__(self, model: FirestoreModel.__class__, required=False):
        super().__init__(model, required=required)


class InvalidValueError(Exception):
    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __str__(self):
        return "InvalidValueError %s is not a valid value for field %s of type %s" %\
            (self.value, self.field.name, self.field.type)


class MalformedQueryError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "MalformedQueryError %s" % self.message


class InvalidPropertyError(Exception):
    def __init__(self, prop_name, model_name):
        self.prop_name = prop_name
        self.model_name = model_name

    def __str__(self):
        return "InvalidPropertyError: %s not found in model %s" % (self.prop_name, self.model_name)
