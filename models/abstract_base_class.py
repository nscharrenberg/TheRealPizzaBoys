from datetime import datetime
from weakref import WeakValueDictionary

from sqlalchemy import inspect
from sqlalchemy.orm import aliased

from app import db


# Inspired by https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json
class MetaBaseModel(db.Model.__class__):
    # Define MetaClass for the BaseModel
    def __init__(self, *args):
        super().__init__(*args)
        self.aliases = WeakValueDictionary()

    def __getitem__(self, key):
        try:
            alias = self.aliases[key]
        except KeyError:
            alias = aliased(self)
            self.aliases[key] = alias
        return alias


class BaseModel:
    print_filter = ()
    to_json_filter = ()

    def __repr__(self):
        # Defining a basway to print models
        return "%s(%s)" % (
            self.__class__.__name__,
            {
                column: value
                for column, value in self._to_dict().items()
                if column not in self.print_filter
            },
        )

    @property
    def json(self):
        return {
            column: value
            if not isinstance(value, datetime)
            else value.strftime("%Y-%m-%d")
            for column, value in self._to_dict().items()
            if column not in self.to_json_filter
        }

    def _to_dict(self):
        # private to_json, allowing overrides without impacting __repr__
        # and being able to add a filter to a lists.
        return {
            column.key: getattr(self, column.key)
            for column in inspect(self.__class__).attrs
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
