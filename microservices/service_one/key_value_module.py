from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from sqlalchemy import *

from microskel.db_module import Base


class KeyValue(Base):  # ORM - Oject - Relational Mapping
    __tablename__ = 'data'
    key = Column(String(128), primary_key=True)
    value = Column(String(1024))

    def __init__(self, key, value):
        self.key = key
        self.value = value


def configure_views(app):
    @app.route('/key_value/<key>', methods=['GET'])
    def key_value(key: str, db: SQLAlchemy):  # db is injected by the injector
        try:
            kv = db.session.query(KeyValue).filter(KeyValue.key == key).one_or_none()
        except NoResultFound as e:
            response = jsonify(status='No such key', context=key)
            response.status = '404'
            return response
        else:
            return jsonify(key=kv.key, value=kv.value) if kv else \
                jsonify(status='No such key', context=key), 404

    @app.route('/key_value', methods=['POST'])
    def create(request: Request, db: SQLAlchemy):
        kv = KeyValue(
            key=request.form.get('key'),
            value=request.form.get('value'))
        db.session.add(kv)
        db.session.commit()
        return 'OK', 201
