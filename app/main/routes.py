from flask import flash, redirect, render_template, request, url_for

from app.main import bp


@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World!"