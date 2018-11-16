
from datetime import datetime, timedelta, timezone
from time import time

from flask_restful import Resource, fields, marshal, reqparse
from ext import db

import uuid

class User( db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    sensors = db.relationship('Sensor', backref='owner', lazy='dynamic')

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(60), index=True)
    stype = db.Column(db.String(30))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    dataset = db.relationship('Data', backref='upper', lazy='dynamic')
    def __repr__(self):
        return '<Sensor {} at {}>'.format(self.id,self.stype)
    def correct(self):
        self.uuid = uuid.uuid4()


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
