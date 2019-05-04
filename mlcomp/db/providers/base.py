from sqlalchemy.orm import joinedload

from mlcomp.db.core import *
from mlcomp.db.models import *
from sqlalchemy.orm.query import Query
from sqlalchemy import desc
from mlcomp.utils.misc import now
from sqlalchemy.orm.attributes import flag_modified, set_attribute
from sqlalchemy import func
from sqlalchemy_serializer import Serializer

class BaseDataProvider:
    model = None

    def __init__(self, session=None):
        if session is None:
            session = Session.create_session()
        self._session = session
        self.serializer = Serializer()

    @property
    def query(self):
        return self.session.query

    def add(self, obj: Base):
        self._session.add(obj)
        return obj

    def by_id(self, id:int):
        return self.query(self.model).filter(getattr(self.model, 'id')==id).first()

    def create_or_update(self, obj: Base, field: str):
        db = self.session.query(obj.__class__).filter(getattr(obj.__class__, field)==getattr(obj, field)).first()
        if db is not None:
            for field, value in obj.__dict__.items():
                if not field.startswith('_'):
                    setattr(db, field, value)
            self.session.update()
        else:
            self.add(obj)

    def update(self):
        self.session.update()

    @property
    def session(self):
        return self._session

    def paginator(self, query: Query, options: PaginatorOptions):
        if options.sort_column:
            column = getattr(self.model, options.sort_column) if \
                options.sort_column in self.model.__dict__ else options.sort_column
            criterion = column if not options.sort_descending else desc(column)
            query = query.order_by(criterion)

        if options.page_size:
            query = query.offset(options.page_size*options.page_number).limit(options.page_size)

        return query

def set_attribute_modified(instance, key, value):
    set_attribute(instance, key, value)
    flag_modified(instance, key)