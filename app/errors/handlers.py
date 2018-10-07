from flask import render_template, make_response,jsonify
from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.app_errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)




