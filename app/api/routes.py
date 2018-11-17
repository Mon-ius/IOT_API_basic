from flask import abort,make_response,g,request
from flask_restful import Resource,  marshal, reqparse
from app.fields import sensor_fields,data_fields,user_fields
from app.models import Sensor,Data,User
from ext import  auth,db,desc

from datetime import datetime, timedelta, timezone
from sqlalchemy import and_

def abort_if_data_doesnt_exist(id,uuid):
    s = Sensor.query.filter_by(uuid=uuid).first()
    if not s :
        abort(400, "Sensor {} doesn't exist".format(uuid))
    d = s.dataset.filter_by(id=id).first()
    if not d :
        abort(400, "Data {} doesn't exist".format(id))
    return d

def abort_if_sensor_doesnt_exist(id):
    s = g.u.sensors.filter_by(id=id).first()
    if not s:
        abort(400, "Sensor {} doesn't exist".format(id))
    return s



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
        u = User.query.filter_by(name=username_or_token).first()
        if not u or not u.verify_password(password):
            return False
    print("--- Login user : " + u.name)
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
        print(u)
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
            abort(400,"Lack enough infomation")

        if User.query.filter_by(name=name).first() is not None:
            abort(400,"User existed")

        u = User(name=name,email=email)
        u.hash_password(password)
        db.session.add(u)
        db.session.commit()

        return {'User': marshal(u, user_fields)}


class SensorAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('uuid', type=str, location='json')
        self.reqparse.add_argument('stype', type=str, location='json')
        super(SensorAPI, self).__init__()

    @auth.login_required
    def get(self, id):
        sensor = abort_if_sensor_doesnt_exist(id)
        return {'sensor': marshal(sensor, sensor_fields)}

    @auth.login_required
    def put(self, id):
        sensor = abort_if_sensor_doesnt_exist(id)
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v != None:
                sensor.__setattr__(k,v)
        db.session.commit()
        return {'sensor': marshal(sensor, sensor_fields)}

    @auth.login_required
    def delete(self, id):
        sensor = abort_if_sensor_doesnt_exist(id)
        db.session.delete(sensor)
        db.session.commit()
        return {'result': marshal(sensor, sensor_fields)}


class SensorListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('stype', type=str, location='json')
        super(SensorListAPI, self).__init__()

    @auth.login_required
    def get(self):
        args = self.reqparse.parse_args()
        ts = Sensor.query.all()
        if not len(ts):
            abort(400, "Sensor doesn't exist")

        sensor = list(map(lambda x: marshal(x, sensor_fields), ts))
        return {'sensors': sensor}

    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        u = g.u
        print(u)
        if not args['stype']:
            abort(400, "Sensor missing stype")
        t = Sensor(owner=u,**args)
        db.session.add(t)
        db.session.commit()
        t.correct()
        print("Sensor",t.__dict__)
        return {'sensor': marshal(t, sensor_fields)}

class DataAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('uuid', type=str, location='json')
        self.reqparse.add_argument('value', type=float, location='json')
        super(DataAPI, self).__init__()

    def get(self, id):
        args = self.reqparse.parse_args()
        data = abort_if_data_doesnt_exist(id,uuid=args['uuid'])

        return {'data': marshal(data, data_fields)}

    def put(self, id):
        args = self.reqparse.parse_args()
        data = abort_if_data_doesnt_exist(id,uuid=args['uuid'])
        for k, v in args.items():
            if v != None:
                data.__setattr__(k,v)
        db.session.commit()
        return {'data': marshal(data, data_fields)}

    def delete(self, id):
        args = self.reqparse.parse_args()
        data = abort_if_data_doesnt_exist(id,uuid=args['uuid'])
        db.session.delete(data)
        db.session.commit()
        return {'result': marshal(data, data_fields)}


class DataListAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('value', type=float, location='json')
        self.reqparse.add_argument('uuid', required=True,type=str, location='json')
        self.reqparse.add_argument('token', type=str, help='No token provided', location='args')
        self.reqparse.add_argument('max', type=str, location='args')
        self.reqparse.add_argument('min', type=str, location='args')
        super(DataListAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        s = Sensor.query.filter_by(uuid=args['uuid']).first()
        if not s:
            abort(400, "Sensor error")
        ts = s.dataset
        if not ts.first():
            abort(400, "data doesn't exist")
        t_type = args['token']
        if t_type:
            if str(t_type)=='v-upper':
                d = ts.order_by(desc(Data.value)).all()
            if str(t_type)=='v-down':
                d = ts.order_by(Data.value).all()
            if str(t_type)=='i-upper':
                d = ts.order_by(desc(Data.id)).all()
            if str(t_type)=='i-down':
                d = ts.order_by(Data.id).all()
            if str(t_type)=='t-upper':
                d = ts.order_by(desc(Data.creation_date)).all()
            if str(t_type)=='t-down':
                d = ts.order_by(Data.creation_date).all()
        d = ts.all()
        data = list(map(lambda x: marshal(x, data_fields), d))

        return {'dataset': data}

    def post(self):
        args = self.reqparse.parse_args()
        s = Sensor.query.filter_by(uuid=args['uuid']).first()
        if not s:
            abort(400, "Sensor error")
        print(s)
        ip = request.remote_addr
        t = Data(ip=ip,value=args['value'],upper=s)

        db.session.add(t)
        db.session.commit()
        t.correct()
        return {'data': marshal(t, data_fields)}


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

