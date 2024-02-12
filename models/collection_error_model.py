from sqlalchemy import Column, Integer, String, create_engine
from flask import current_app
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from res import DatabaseError
from . import db

class CollectionError (db.Model):
    __tablename__ = 'app_collection_errors'

    id = Column(Integer, primary_key=True)
    collection_name = Column(String)

    def __init__(self, data):
        for key, item in data.items():
            setattr(self, key, item)
    
    def save(self):   
        with current_app.app_context():
            try:
                db.session.add(self)
                db.session.commit()
            except SQLAlchemyError as err:
                raise DatabaseError("Database Error", err)
            except Exception as err:
                raise Exception("Internal Error", err)

    def __repr__(self):
        return f'<CollectionError {self.collection_name}>'