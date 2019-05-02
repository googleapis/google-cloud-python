from google.cloud.firestore_v1beta1.client import Client, DEFAULT_DATABASE


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


class FirestoreModel:
    def __init__(self, __project=None, __credentials=None, __database=DEFAULT_DATABASE, **data):
        self.__setup_fields()
        self.__db = Client(project=__project, credentials=__credentials, database=__database)
        self.__model_name = type(self).__name__
        self.__collection = self.__db.collection(self.__model_name)
        self.id = None
        if "id" in data:
            self.id = data.pop("id")
        for key, value in data.items():
            if key in self.fields:
                setattr(self, key, value)

    def __str__(self):
        return "<Model %s>" % self.__model_name

    def __setup_fields(self):
        self.fields = dict()
        for attribute in dir(self):
            if attribute.startswith("_"):
                continue
            value = getattr(self, attribute)
            if isinstance(value, _Field):
                value.name = attribute
                self.fields[attribute] = value
                setattr(self, attribute, value.default)

    def __prepare(self):
        values = dict()
        for key, field in self.fields.items():
            value = getattr(self, key)
            field.validate(value)
            values[key] = value
        return values

    def put(self):
        data = self.__prepare()
        if self.id:
            self.__collection.document(self.id).set(data)
            return True
        _time, new_ref = self.__collection.add(data)
        self.id = new_ref.id
        return True

    @classmethod
    def get(cls, key_id: str):
        db = Client().collection(cls.__name__).document(key_id)
        data = db.get()
        if not data.exists:
            return None
        return cls(id=key_id, **data.to_dict())

    @classmethod
    def query(cls, offset=0, limit=0):
        class Query(object):
            def __init__(self, model, _offset, _limit):
                self.__collection = Client().collection(model.__name__)
                self.offset = _offset
                self.limit = _limit
                self.cursor = 0
                self.__fetch_pos = 0

            def where(self, field, value, operand="=="):
                self.__collection.filter(field, operand, value)
                return self

            def __fetch(self):
                # Only keep 100 a maximum of 100 records in memory all the time
                self.__collection.query()

            def __iter__(self):
                self.cursor += 1

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
        return "%s is not a valid value for field %s of type %s" %\
            (self.value, self.field.name, self.field.type)
