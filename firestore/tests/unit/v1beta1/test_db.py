from unittest import TestCase
from google.cloud.firestore_v1beta1 import db, SERVER_TIMESTAMP
import json
from datetime import datetime, date


"""
A group meet ups organizing app that allow users add meetups and to RSVP to meetups
"""


class User(db.FirestoreModel):
    """A user can register and can have an account in multiple groups"""
    name = db.StringField(default="doe")
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    date_registered = db.DateTimeField(auto_add_now=True)


class Group(db.FirestoreModel):
    """A group is created by a user and can be invite only or public"""
    name = db.StringField()
    description = db.StringField(length=400)
    creator = db.ReferenceField(model=User)
    date_created = db.DateTimeField(auto_add_now=True)
    last_update = db.DateTimeField(auto_now=True)
    public_group = db.BooleanField(default=True)


class Account(db.FirestoreModel):
    """An account exists in a group, belongs to a user"""
    __sub_collection__ = Group
    user = db.ReferenceField(model=User)
    roles = db.ListField(field_type=db.StringField(required=True))
    date_joined = db.DateTimeField(auto_add_now=True)


class Meetup(db.FirestoreModel):
    """Meetups that are only open and accessible to members of a group"""
    __sub_collection__ = Group
    organizer = db.ReferenceField(Account, required=True)  # This Account must belong to the same group
    title = db.StringField(length=200)
    description = db.StringField()
    date_created = db.DateTimeField(auto_add_now=True)
    meetup_date = db.DateTimeField()


class RSVP(db.FirestoreModel):
    """RSVP to attend a private meetup"""
    account = db.ReferenceField(Account, required=True)
    meetup = db.ReferenceField(Meetup)
    rsvp_date = db.DateTimeField(auto_add_now=True)


class Conversation(db.FirestoreModel):
    """Conversations between users"""
    users = db.ListField(field_type=db.ReferenceField(model=User, required=True))
    start_time = db.DateTimeField(auto_add_now=True)
    last_update = db.DateTimeField(auto_now=True)

    def send_message(self, user, text):
        if user not in self.users:
            raise Exception("User must be in a conversation to send a message")
        message = MessageLog(__parent__=self, sender=user, message=text)
        message.put()


class MessageLog(db.FirestoreModel):
    """Actual messages between users in a conversation"""
    __sub_collection__ = Conversation
    sender = db.ReferenceField(User, required=True)
    message = db.StringField()
    date_sent = db.DateTimeField(auto_add_now=True)


class DoomedToFail(db.FirestoreModel):
    """This model should never initialize. We're referencing a Model that we can't tell the parent"""
    message = db.ReferenceField(MessageLog)


class TestDB(TestCase):
    def setUp(self):
        class John:
            name = "John Doe"
            email = "john@doe.fam"
            password = "stupidJane"

        class Jane:
            name = "Jane Doe"
            email = "jane@doe.fam"
            password = "StewPidJohn"
        self.john = John
        self.jane = Jane

    def test_fields(self):
        # String Field
        string_field = db.StringField(default="test", required=True, length=6)
        self.assertEqual(string_field.validate("roast"), "roast")
        # The default value is set on an empty field
        self.assertEqual(string_field.validate(None), "test")
        # The string requires a maximum length of 6
        self.assertRaises(db.InvalidValueError, string_field.validate, "01234567")
        #  String field should only accept strings
        self.assertRaises(db.InvalidValueError, string_field.validate, 123)
        # Create a field without a default value
        string_field = db.StringField(required=True)
        # This is a required field, None is not a valid value
        self.assertRaises(db.InvalidValueError, string_field.validate, None)

        # Integer field
        integer_field = db.IntegerField()
        self.assertEqual(integer_field.validate(1), 1)
        self.assertEqual(integer_field.validate(0), 0)
        # Float is not a valid value of an integer field
        self.assertRaises(db.InvalidValueError, integer_field.validate, 1.36)
        # String is not a valid integer
        self.assertRaises(db.InvalidValueError, integer_field.validate, "0")
        # None required field defaults to None
        self.assertIsNone(integer_field.validate(None))

        # Float field
        float_field = db.FloatingPointNumberField()
        # Should accept both float and integer values
        self.assertEqual(float_field.validate(0), 0)
        self.assertEqual(float_field.validate(1), 1)
        self.assertEqual(float_field.validate(0.6667), 0.6667)
        self.assertEqual(float_field.validate(3.142), 3.142)
        self.assertRaises(db.InvalidValueError, float_field.validate, "10234")

        # List Field
        list_field = db.ListField(field_type=db.IntegerField())
        self.assertEqual(list_field.validate([1, 2, 3, 4]), [1, 2, 3, 4])
        # An invalid data type is not accepted as part of the child fields
        self.assertRaises(db.InvalidValueError, list_field.validate, [1, 2, ""])

        # Dict Field
        dict_field = db.DictField()
        valid_dict = dict(name="John doe", age=24)
        # A dict, a list, or a valid json string are valid values
        self.assertEqual(dict_field.validate(valid_dict), valid_dict)
        self.assertEqual(dict_field.validate(json.dumps(valid_dict)), valid_dict)
        # A list is not a valid input of dict field
        self.assertRaises(db.InvalidValueError, dict_field.validate, [1, 2, 3])

        # Date time Field
        dt_field = db.DateTimeField(auto_add_now=True)
        now = datetime.now()
        self.assertEqual(dt_field.validate(now), now)
        # Confirm that default is set to server timestamp
        self.assertEqual(dt_field.validate(None), SERVER_TIMESTAMP)
        # A string is not a date time object
        self.assertRaises(db.InvalidValueError, dt_field.validate, "12-may-2019")
        today = now.date()
        # A date item is a valid entry
        self.assertIsInstance(today, date)
        self.assertEqual(dt_field.validate(today), today)
        dt_field = db.DateTimeField(auto_now=True)
        # This value is always updated to current time stamp on every update
        self.assertEqual(dt_field.validate(now), SERVER_TIMESTAMP)

        # Boolean field
        bool_field = db.BooleanField(required=True)
        self.assertTrue(bool_field.validate(True))
        self.assertFalse(bool_field.validate(False))
        self.assertRaises(db.InvalidValueError, bool_field.validate, "some string")
        self.assertRaises(db.InvalidValueError, bool_field.validate, None)  # None is not a valid boolean value
        bool_field = db.BooleanField()
        self.assertIsNone(bool_field.validate(None))

        # Bytes field
        some_bytes = bytes(b"bavnkvnkjwenegkv,erngvanavnwisnkversnvaern")
        bytes_field = db.BytesField(default=some_bytes)
        other_bytes = bytes(b"qwertytuyioutryewwertyrytuyterwqwewqrwetry")
        self.assertEqual(bytes_field.validate(None), some_bytes)
        self.assertEqual(bytes_field.validate(other_bytes), other_bytes)
        self.assertRaises(db.InvalidValueError, bytes_field.validate, "some_string")

    def test_reference_field(self):
        jane = User(name=self.jane.name, email=self.jane.email, password=self.jane.password)
        john = User(name=self.john.name, email=self.john.email, password=self.john.password)

    def test_model_initialization(self):
        jane = User(name="Jane Doe", email="jane@doe.fam", password="stupidJohn")
        self.assertEqual(jane.name, "Jane Doe")
        self.assertEqual(jane.email, "jane")
        self.assertEqual(jane.password, "Jane Doe")
