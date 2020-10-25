from mongoengine import *

from Helpers.BaseDocument import BaseDocument


class TrolleyModel(BaseDocument):
    trolley_id = StringField()
    recorded_date_time = DateTimeField()
    temperature = IntField()
