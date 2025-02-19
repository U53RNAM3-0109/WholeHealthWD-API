from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, DateTime, func

class BaseIDandTableName(object):
    @declared_attr
    def __tablename__(cls):
        return str(cls.__name__).lower().replace("model","")

    id = Column(Integer, primary_key=True, autoincrement=True)

class TimestampLastEditMixin(object):
    last_edit = Column(DateTime, default=func.now(), onupdate=func.now())

class TimestampCreatedMixin(object):
    created_at = Column(DateTime, default=func.now())