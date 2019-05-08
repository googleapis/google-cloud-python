from unittest import TestCase, mock
from google.cloud.firestore_v1beta1 import db


class UserModel(db.FirestoreModel):
    name = db.StringField(required=True)
    age = db.IntegerField()
    tags = db.ListField(db.StringField)



class Messages(db.FirestoreModel):
    user = db.ReferenceField(UserModel)


class TestDB(TestCase):
    def test_fox(self):
        print("pass")
        user = UserModel.get("billcountry")
        user.name = "Billcountry Mwaniki"
        user.age = 24
        user.put()


