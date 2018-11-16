from flask import abort,make_response,g
from flask_restful import Resource,  marshal, reqparse
from app.fields import sensor_fields,data_fields,user_fields
from app.models import Sensor,Data,User
from ext import  auth,db,desc

from datetime import datetime, timedelta, timezone
from sqlalchemy import and_

def abort_if_sensor_doesnt_exist(id):
    s = Sensor.query.filter_by(id=id).first()
    if not s:
        abort(400, "Sensor {} doesn't exist".format(id))
    return s

def abort_if_data_doesnt_exist(id):
    d = Data.query.filter_by(id=id).first()
    if not d :
        abort(400, "Data {} doesn't exist".format(id))
    return d


def abort_if_user_doesnt_exist(name):
    u = User.query.filter_by(name=name).first()
    if not u:
        abort(400, "User {} doesn't exist".format(name))
    return u


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@auth.verify_password
def verify_password(username_or_token, password):
    u = User.verify_auth_token(username_or_token)
    
    if not u:
        # try to authenticate with username/password
        u = User.query.filter_by(username=username_or_token).first()
        if not u or not u.verify_password(password):
            return False
    print("--- Login user : " + u.username)
    g.u = u
    return True


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name', type=str, location='json')
        self.reqparse.add_argument(
            'email', type=str, location='json')
        self.reqparse.add_argument(
            'password', type=str, location='json')
        super(UserAPI, self).__init__()

    @auth.login_required
    def get(self):
        u = g.u
        return {'User': marshal(u, user_fields)}

    @auth.login_required
    def put(self):
        u = g.u
        token = u.generate_auth_token()
        return {'token': token.decode('ascii'), 'duration': 600}

    def post(self):
        args = self.reqparse.parse_args()
        name = args['name']
        email = args['email']
        password = args['password']

        if not name  or  not password or not email:
            abort(400)

        if User.query.filter_by(name=name).first() is not None:
            abort(400)

        u = User(name=name,email=email)
        u.hash_password(password)
        db.session.add(stu)
        db.session.commit()

        return {'User': marshal(u, user_fields)}


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
