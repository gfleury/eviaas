from sqlalchemy import Column, ForeignKey, Integer, String, TypeDecorator
from sqlalchemy.orm import relationship
from evi.serializer import Serializer
from evi import db
from plan import Plan

class Instance(db.Model, Serializer):
    __tablename__ = 'instance'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    team = Column(String(50), nullable=False)
    user = Column(String(50), nullable=False)
    plan_id = Column(Integer, ForeignKey('plan.id'), nullable=False)
    plan = relationship(Plan)

    def __init__(self, json):
        for i in json:
            setattr(self, i, json[i])

    def serialize(self):
        d = Serializer.serialize(self)
        del d['id']
        d['plan'] = Serializer.serialize(d['plan'])
        return d