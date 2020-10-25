import json
import uuid
from datetime import datetime

from mongoengine import *

DATE_TIME_FORMAT = "%m:%d:%Y %H:%M:%S"


# Mongodb ODM Model
class BaseDocument(Document):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    # created_by = str(g.get('user')["id"]) if g.get('user') else ""
    key = UUIDField(binary=False, default=uuid.uuid4())

    meta = {
        'abstract': True,
    }

    @staticmethod
    def not_empty(value):
        if not value:
            raise ValidationError("can not be empty")
        return value

    def get_id_from_response(self, response):
        id = response.get('_id') or response.get('_auto_id_0')
        if type(id) == dict:
            return id['$oid']
        return id

    def to_json(self, *args, **kwargs):
        response = super().to_json()
        response = json.loads(response)

        if response:
            response['id'] = self.get_id_from_response(response)

            keys = list(response.keys())
            if '_id' in keys:
                del response['_id']
            if '_auto_id_0' in keys:
                del response['_auto_id_0']

        response['created_at'] = self.str_or_date(self.created_at)
        response['updated_at'] = self.str_or_date(self.updated_at)
        return response

    def str_or_date(self, date):
        if type(date) == str:
            return date
        return date.strftime(DATE_TIME_FORMAT)

    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):

        self.updated_at = datetime.now().strftime(DATE_TIME_FORMAT)
        print("saving ", kwargs)
        super().save(kwargs, validate=False)
