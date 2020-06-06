from flask import request, jsonify, session, url_for, redirect, Blueprint

from app.main.utils.youtube_api.google_auth import get_authorization_url, exchange_code_for_credentials


authorization = Blueprint('authorization', __name__)

@authorization.route('/authorize', methods=['GET'])
def authorize():
    print(url_for('authorization.oauth2callback'))
    authorization_url, state = get_authorization_url(url_for('authorization.oauth2callback', _external=True))

    session['state'] = state

    return jsonify(authorization_url)



@authorization.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    
    session['credentials'] = exchange_code_for_credentials(url_for('authorization.oauth2callback', _external=True), request.url)

    return {
        'message_code': 200,
        'message': "Google oauth2 done."
    }
