from flask import abort
from flask_restful import Resource,  marshal, reqparse
from app.fields import sensor_fields,data_fields
from app.models import Sensor,Data
from ext import  db,desc

from datetime import datetime, timedelta, timezone
from sqlalchemy import and_

def abort_if_sensor_doesnt_exist(id):
    ss = Sensor.query.filter_by(id=id).first()
    if not ss:
        abort(400, "Sensor {} doesn't exist".format(id))
    return ss

def abort_if_data_doesnt_exist(id):
    dat = Data.query.filter_by(id=id).first()
    if not dat :
        abort(400, "Data {} doesn't exist".format(id))
    return dat

class SensorAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('uuid', type=str, location='json')
        self.reqparse.add_argument('type', type=str, location='json')
        super(SensorAPI, self).__init__()

    def get(self, id):
        sensor = abort_if_sensor_doesnt_exist(id)
        return {'sensor': marshal(sensor.__dict__, sensor_fields)}

    def put(self, id):
        sensor = abort_if_sensor_doesnt_exist(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                sensor.__setattr__(k,v)
        db.session.commit()
        return {'sensor': marshal(sensor.__dict__, sensor_fields)}

    def delete(self, id):
        sensor = abort_if_sensor_doesnt_exist(id)
        db.session.delete(sensor)
        db.session.commit()
        return {'result': marshal(sensor.__dict__, sensor_fields)}


class SensorListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('type', type=str, location='json')
        super(SensorListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        ts = Sensor.query.all()
        if not len(ts):
            abort(400, "Sensor doesn't exist")

        sensor = list(map(lambda x: marshal(x.__dict__, sensor_fields), ts))
        return {'sensors': sensor}

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        val = args
        t = Sensor(**val)
        db.session.add(t)
        db.session.commit()
        t.correct()
        return {'sensor': marshal(t.__dict__, sensor_fields)}

class DataAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('uuid', type=str, location='json')
        self.reqparse.add_argument('value', type=float, location='json')
        super(DataAPI, self).__init__()

    def get(self, id):
        data = abort_if_data_doesnt_exist(id)
        return {'data': marshal(data.__dict__, data_fields)}

    def put(self, id):
        data = abort_if_data_doesnt_exist(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                data.__setattr__(k,v)
        db.session.commit()
        return {'data': marshal(data.__dict__, data_fields)}

    def delete(self, id):
        data = abort_if_data_doesnt_exist(id)
        db.session.delete(data)
        db.session.commit()
        return {'result': marshal(data.__dict__, data_fields)}


class DataListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('value', type=float, location='json')
        self.reqparse.add_argument('uuid', type=str, location='json')
        self.reqparse.add_argument('token', type=str, help='No token provided', location='args')
        self.reqparse.add_argument('max', type=str, location='args')
        self.reqparse.add_argument('min', type=str, location='args')
        super(DataListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        ts = data.query.all()
        if not len(ts):
            abort(400, "data doesn't exist")
        t_type = args['token']
        if t_type:
            if str(t_type)=='v-upper':
                ts = data.query.order_by(desc(data.value)).all()
            if str(t_type)=='v-down':
                ts = data.query.order_by(data.value).all()
            if str(t_type)=='i-upper':
                ts = data.query.order_by(desc(data.id)).all()
            if str(t_type)=='i-down':
                ts = data.query.order_by(data.id).all()
            if str(t_type)=='t-upper':
                ts = data.query.order_by(desc(data.creation_date)).all()
            if str(t_type)=='t-down':
                ts = data.query.order_by(data.creation_date).all()

        data = list(map(lambda x: marshal(x.__dict__, datas_fields), ts))

        return {'datas': data}

    def post(self):
        args = self.reqparse.parse_args()
        val = args
        val.pop('token')
        val.pop('min')
        val.pop('max')
        t = data(**val)
        db.session.add(t)
        db.session.commit()
        t.correct()
        return {'data': marshal(t.__dict__, datas_fields)}


class OpenRes(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'id', type=str, location='json')
        super(OpenRes, self).__init__()

    def get(self):

        return {'message': "get success"}
        

    def post(self):
        args = self.reqparse.parse_args()
        message = args['id']

        return {'message': message}

    def put(self):
        args = self.reqparse.parse_args()
        message = args['id']

        return {'message': "put success"}

    def delete(self):
        return {'message': "delete success"}
