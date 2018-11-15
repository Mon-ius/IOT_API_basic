from flask import abort
from flask_restful import Resource,  marshal, reqparse
from app.fields import temp_fields, temps_fields,light_fields, lights_fields
from app.models import Temperature,Light
from ext import  db,desc

from datetime import datetime, timedelta, timezone


def abort_if_temp_doesnt_exist(id):
    temp = Temperature.query.filter_by(id=id).first()
    if not temp:
        abort(400, "Temperature {} doesn't exist".format(id))
    return temp

def abort_if_light_doesnt_exist(id):
    temp = Temperature.query.filter_by(id=id).first()
    if not temp:
        abort(400, "Light {} doesn't exist".format(id))
    return temp

class TemperatureAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('value', type=str, location='json')
        self.reqparse.add_argument('place', type=str, location='json')
        super(TemperatureAPI, self).__init__()

    def get(self, id):
        temp = abort_if_temp_doesnt_exist(id)
        return {'temp': marshal(temp, temp_fields)}

    def put(self, id):
        temp = abort_if_temp_doesnt_exist(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                temp.__setattr__(k,v)
        db.session.commit()
        return {'temp': marshal(temp, temp_fields)}

    def delete(self, id):
        temp = abort_if_temp_doesnt_exist(id)
        db.session.delete(temp)
        db.session.commit()
        return {'result': marshal(temp, temp_fields)}


class TemperatureListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('value', type=str, location='json')
        self.reqparse.add_argument('place', type=str, location='json')
        self.reqparse.add_argument('token', type=str, help='No token provided', location='args')
        super(TemperatureListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        ts = Temperature.query.all()
        if not len(ts):
            abort(400, "Temperature doesn't exist")
        t_type = args['token']
        if t_type:
            if str(t_type)=='v-upper':
                ts = Temperature.query.order_by(desc(Temperature.value)).all()
            if str(t_type)=='v-down':
                ts = Temperature.query.order_by(Temperature.value).all()
            if str(t_type)=='i-upper':
                ts = Temperature.query.order_by(desc(Temperature.id)).all()
            if str(t_type)=='i-down':
                ts = Temperature.query.order_by(Temperature.id).all()
            if str(t_type)=='t-upper':
                ts = Temperature.query.order_by(desc(Temperature.creation_date)).all()
            if str(t_type)=='t-down':
                ts = Temperature.query.order_by(Temperature.creation_date).all()

        temp = list(map(lambda x: marshal(x.__dict__, temps_fields), ts))
        return {'temps': temp}

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        val = args
        val.pop('token')
        t = Temperature(**val)
        db.session.add(t)
        db.session.commit()
        t.correct()
        return {'temp': marshal(t.__dict__, temps_fields)}

class LightAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('value', type=str, location='json')
        self.reqparse.add_argument('place', type=str, location='json')
        super(LightAPI, self).__init__()

    def get(self, id):
        light = abort_if_light_doesnt_exist(id)
        return {'light': marshal(light, light_fields)}

    def put(self, id):
        light = abort_if_light_doesnt_exist(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                light.__setattr__(k,v)
        db.session.commit()
        return {'light': marshal(light, light_fields)}

    def delete(self, id):
        light = abort_if_light_doesnt_exist(id)
        db.session.delete(light)
        db.session.commit()
        return {'result': marshal(light, light_fields)}


class LightListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('value', type=str, location='json')
        self.reqparse.add_argument('token', type=str, help='No token provided', location='args')
        self.reqparse.add_argument('place', type=str, location='json')
        super(LightListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        ts = Light.query.all()
        if not len(ts):
            abort(400, "Light doesn't exist")
        t_type = args['token']
        if t_type:
            if str(t_type)=='v-upper':
                ts = Light.query.order_by(desc(Light.value)).all()
            if str(t_type)=='v-down':
                ts = Light.query.order_by(Light.value).all()
            if str(t_type)=='i-upper':
                ts = Light.query.order_by(desc(Light.id)).all()
            if str(t_type)=='i-down':
                ts = Light.query.order_by(Light.id).all()
            if str(t_type)=='t-upper':
                ts = Light.query.order_by(desc(Light.creation_date)).all()
            if str(t_type)=='t-down':
                ts = Light.query.order_by(Light.creation_date).all()

        light = list(map(lambda x: marshal(x.__dict__, lights_fields), ts))

        return {'lights': light}

    def post(self):
        args = self.reqparse.parse_args()
        val = args
        val.pop('token')
        t = Light(**val)
        db.session.add(t)
        db.session.commit()
        t.correct()
        return {'light': marshal(t.__dict__, lights_fields)}


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
