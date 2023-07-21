import uuid
import datetime as dt
import logging
import humps
import sqlalchemy as sa

from source.database import db

log = logging.getLogger(__name__)


class BaseMixInModel(object):
    def __iter__(self):
        for x in self.__class__.__table__.columns:
            yield x.name, self.__getattribute__(x.name)

    def __str__(self):
        fields = [f"{k}={v}" for k, v in dict(self).items() if k != "id"]
        str_fields = ", ".join(fields)
        return f"<{self.__class__.__name__} {self.id} ({str_fields})>"

    def __repr__(self):
        return str(self)

    @classmethod
    def get(cls, obj_id, key="id"):
        try:
            return db.session.query(cls).filter(getattr(cls, key) == obj_id).first()
        except sa.orm.exc.NoResultFound as e:
            log.debug(f"{e.__class__.__name__}: {e}")
            raise Exception(cls.__name__, "ID")

    @classmethod
    def get_all_by_id(cls, obj_id, key="id"):
        try:
            return db.session.query(cls).filter(getattr(cls, key) == obj_id).all()
        except sa.orm.exc.NoResultFound as e:
            log.debug(f"{e.__class__.__name__}: {e}")
            raise Exception(cls.__name__, "ID")

    # @classmethod
    # def get_by_name(cls, name):
    #     try:
    #         return db.session.query(cls).filter(cls.nome == name).first()
    #     except Exception as e:
    #         return None
    #         # raise Exception(cls.__name__, e)

    @classmethod
    def get_all(cls):
        has_is_deleted_attribute = hasattr(cls, "is_deleted")
        if has_is_deleted_attribute:
            return (
                db.session.query(cls).filter(getattr(cls, "is_deleted") == False).all()
            )
        return db.session.query(cls).all()

    @staticmethod
    def json_type(x):
        if isinstance(x, dt.datetime):
            return x.timestamp()
        return x

    def json(self, camelize=True, exclude=()):
        response = {
            k: str(v) if isinstance(v, uuid.UUID) else self.json_type(v)
            for k, v in dict(self).items()
            if k not in exclude
        }

        if camelize:
            response = humps.camelize(response)

        return response
