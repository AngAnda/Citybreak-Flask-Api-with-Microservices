from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from sqlalchemy import *
from datetime import datetime

from microskel.db_module import Base


class Event(Base):
    __tablename__ = 'service_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(128))
    name = Column(String(256))
    date = Column(Date)
    description = Column(Text())

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'name': self.name,
            'date': self.date.isoformat() if self.date else None,  # Convert date to string
            'description': self.description
        }

def configure_views(app):
    @app.route('/service_events/<int:id>', methods=['GET'])
    def get(id:int, db:SQLAlchemy):
        try:
            ev = db.session.query(Event).filter(Event.id == id).one_or_none()
        except NoResultFound as e:
            response = jsonify(status='No such key', context=id)
            response.status = '404'
            return response
        else:
            return ev.to_dict() if ev else \
                jsonify(status='No such key', context=id), 404


    @app.route('/service_events', methods=['POST'])
    def create(request: Request, db: SQLAlchemy):
        data = request.form
        ev = Event(
            city=data.get('city'),
            name=data.get('name'),
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date() if data.get('date') else None,
            description=data.get('description')
        )

        db.session.add(ev)
        db.session.commit()
        return 'OK', 201

    @app.route('/test')
    def test():
        print('test123')