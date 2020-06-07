from flask import request, jsonify, session, url_for, redirect, Blueprint


error = Blueprint('error', __name__)

@error.app_errorhandler(404)
def page_not_found(error):
    return jsonify(
        {
            'status': 404,
            'error': 'ressource not found'
        }
    )