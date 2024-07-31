from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, Injector, Binder, singleton
from sqlalchemy.orm import declarative_base
from decouple import config

Base = declarative_base()

class DatabaseModule(Module):
    def __init__(self, app: Flask):
        self.app = app
        self.base = Base
        self.app.config['SQLALCHEMY_DATABASE_URI'] = config('MICROSERVICE_DB_URI')
        # TODO

    def configure(self, binder: Binder) -> None:
        db = self.configure_db()
        binder.bind(SQLAlchemy, to=db, scope=singleton)

    def configure_db(self):
        db = SQLAlchemy(self.app)
        self.base.metadata.create_all(db.engine)
        return db


def configure_views(app):
    pass
