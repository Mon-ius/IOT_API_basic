from flask import abort
from flask_restful import Resource,  marshal, reqparse
from app.fields import temp_fields, temps_fields
from app.models import Temperature
from ext import  db

from datetime import datetime, timedelta, timezone


def abort_if_temp_doesnt_exist(id):
    temp = Temperature.query.filter_by(id=id).first()
    if not temp:
        abort(400, "Temperature {} doesn't exist".format(id))
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
        super(TemperatureListAPI, self).__init__()

    def get(self):
        ts = Temperature.query.all()
        if not len(ts):
            abort(400, "Temperature doesn't exist")
        temp = list(map(lambda x: marshal(x.__dict__, temps_fields), ts))

        return {'temps': temp}

    def post(self):
        args = self.reqparse.parse_args()
        t = Temperature(**args)
        db.session.add(t)
        db.session.commit()
        t.correct()
        return {'temp': marshal(t.__dict__, temps_fields)}


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
