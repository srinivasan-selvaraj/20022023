from app import db
from datetime import datetime,timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

    
class Parents(db.Model):
    __tablename__ = 'parents'
    id = db.Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = db.Column(String(50))
    
class Childs(db.Model):
    __tablename__ = 'childs'
    id = db.Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    name = db.Column(String(50))
    
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    parents = db.relationship("Parents", backref=backref("child_parent", uselist=False))

class ManyRelated(db.Model):
    __tablename__ = 'many_related'
    id = db.Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'))
    parents = db.relationship("Parents", backref=backref("parents", uselist=False))

    child_id1 = db.Column(db.Integer, db.ForeignKey('childs.id'))
    # child1 = db.relationship("Childs", backref=backref("childs", uselist=False))

    child_id2 = db.Column(db.Integer, db.ForeignKey('childs.id'))
    # child2 = db.relationship("Childs", backref=backref("childs", uselist=False))


