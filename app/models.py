
from datetime import datetime, timedelta, timezone
from time import time

from flask_restful import Resource, fields, marshal, reqparse
from ext import db

class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(80))
    place = db.Column(db.String(120))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Temperature {} at {} in {}>'.format(self.value,self.place,str(self.creation_date)[:10])
    def correct(self):
        self.id=self.id

class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(80))
    place = db.Column(db.String(120))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Light {} at {} in {}>'.format(self.value,self.place,str(self.creation_date)[:10])
    def correct(self):
        self.id=self.id

