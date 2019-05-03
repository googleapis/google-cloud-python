from unittest import TestCase
from google.cloud.firestore_v1beta1 import db


class TestModel(db.FirestoreModel):
    name = db.StringField(required=True)
    age = db.IntegerField()
    tags = db.ListField(db.StringField)


class TestDB(TestCase):
    pass
