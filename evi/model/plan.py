from sqlalchemy import Column, ForeignKey, Integer, String, TypeDecorator
from sqlalchemy.orm import relationship
from Crypto.Cipher import AES
import binascii
from evi.serializer import Serializer
from evi import db

key = bytes('keyzzzzzzzzzzzzz')

def aes_encrypt(data):
    cipher = AES.new(key)
    data = data + (" " * (16 - (len(data) % 16)))
    return binascii.hexlify(cipher.encrypt(data))

def aes_decrypt(data):
    cipher = AES.new(key)
    return cipher.decrypt(binascii.unhexlify(data)).rstrip()


class EncryptedValue(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        return aes_encrypt(value)

    def process_result_value(self, value, dialect):
        return aes_decrypt(value)


class Plan(db.Model, Serializer):
    __tablename__ = 'plan'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(250), nullable=False)

    def __init__(self, json):
        for i in json:
            setattr(self, i, json[i])

    def serialize(self):
        d = Serializer.serialize(self)
        del d['id']
        return d

class Env(db.Model, Serializer):
    __tablename__ = 'env'
    id = Column(Integer, primary_key=True)
    key = Column(String(250), nullable=False, unique=True)
    value = Column(EncryptedValue(500), nullable=False)
    plan_id = Column(Integer, ForeignKey('plan.id'))
    plan = relationship(Plan)

    def __init__(self, json):
        for i in json:
            setattr(self, i, json[i])

    def serialize(self):
        d = Serializer.serialize(self)
        del d['plan']
        del d['plan_id']
        del d['id']
        return d

    @staticmethod
    def serialize_json(l):
        serialized_dict = {}
        for m in l:
            serialized_dict.update({m.key: m.value})
        return serialized_dict