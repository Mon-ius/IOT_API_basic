
from datetime import datetime, timedelta, timezone
from time import time

from flask_restful import Resource, fields, marshal, reqparse
from ext import db
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import check_password_hash, generate_password_hash

from flask import current_app
import uuid
    
class User( db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    sensors = db.relationship('Sensor', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)

        except SignatureExpired:

            return None    # valid token, but expired
        except BadSignature:

            return None    # invalid token
        u = User.query.get(data['id'])
        return u

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(60), index=True, default=str(uuid.uuid1()))
    stype = db.Column(db.String(30))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dataset = db.relationship('Data', backref='upper', lazy='dynamic')

    def __repr__(self):
        return '<Sensor {} at {}>'.format(self.id,self.stype)
    def correct(self):
        self.id = self.id


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float())
    ip = db.Column(db.String(120))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    def __repr__(self):
        return '<Data{} {} at {} in {}>'.format(self.id,self.value,str(self.creation_date)[:10],self.ip)
    def correct(self):
        self.id=self.id

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float())
    place = db.Column(db.String(120))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Temp{} at {}>'.format(self.value,self.place)
    def correct(self):
        self.id=self.id