from flask import flash, redirect, render_template, request, url_for,send_from_directory,current_app
from app.api.routes import SensorListAPI,DataListAPI
from app.main import bp
from flask_restful import Api

@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def index():
    auth = url_for('main.index',  _external=True)+'api/users'
    return render_template('main/index.html', title='Home',auth=auth)

@bp.route('/relationship', methods=['GET', 'POST'])
def relationship():
    auth = url_for('main.index',  _external=True)+'api/users'
    return render_template('main/relationship.html', title='Relationship',auth=auth)

@bp.route('/chart', methods=['GET', 'POST'])
def chart():
    auth = url_for('main.index',  _external=True)+'api/users'
    tmp  = url_for('main.index',  _external=True)+'api/temps'
    light  = url_for('main.index',  _external=True)+'api/lights'
    return render_template('main/chart.html', title='Chart',tmp=tmp,light=light,auth=auth)

@bp.route('/mannual', methods=['GET', 'POST'])
def mannual():
    auth = url_for('main.index',  _external=True)+'api/users'
    tmp  = url_for('main.index',  _external=True)+'api/temps'
    light  = url_for('main.index',  _external=True)+'api/lights'
    return render_template('main/mannual.html', title='mannual',tmp=tmp,light=light,auth=auth)
    # return render_template('main/mannual.html', title='mannual',tmp=tmp,light=light)

@bp.route('/table', methods=['GET', 'POST'])
def table():
    auth = url_for('main.index',  _external=True)+'api/users'
    tmp  = url_for('main.index',  _external=True)+'api/temps'
    return render_template('main/table.html', title='Table',tmp=tmp,auth=auth)




