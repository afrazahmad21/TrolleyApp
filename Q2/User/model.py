from mongoengine import *

from Helpers.BaseDocument import BaseDocument


class User(BaseDocument):
    email = StringField()
    password = StringField()
