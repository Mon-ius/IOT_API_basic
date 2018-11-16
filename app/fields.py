from flask_restful import fields

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'last_seen': fields.DateTime
}

sensor_fields = {
    'id': fields.Integer,
    'uuid': fields.String,
    'stype': fields.String
}

data_fields = {
    'id': fields.Integer,
    'value': fields.Float,
    'ip': fields.String,
    'creation_date': fields.DateTime
}




