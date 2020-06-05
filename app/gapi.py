import os

import google_auth_oauthlib.flow
import google.oauth2.credentials

import googleapiclient.discovery

from flask import Flask, request, jsonify, session, url_for, redirect

app = Flask(__name__)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.secret_key = b'\xf9\xa6~\xd8\xc0\xe4\xd78\xe6\xceqv\xb2\xc6<\xdf'

basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/authorize', methods=['GET'])
def authorize():


    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('code_secret_client.json', 
        [
            'https://www.googleapis.com/auth/youtube.force-ssl',
        ]
    )

    flow.redirect_uri = url_for("oauth2callback", _external=True)
    print(url_for('oauth2callback', _external=True))

    authorization_url, state = flow.authorization_url(
        include_granted_scopes='true',
        state="statevalue",
        prompt='consent',

    )

    session['state'] = state

    return jsonify(authorization_url)

@app.route('/oauth2callback', methods=['GET'])
def oauth2callback():
    state = session['state']
    print(state)
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'code_secret_client.json',
        [
            'https://www.googleapis.com/auth/youtube.force-ssl',
        ]
    )
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url

    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return {
        'message_code': 200,
        'message': "Google oauth2 done."
    }


@app.route('/subscription', methods=['GET'])
def get_subscriptions():
    # Check if user is logged in
    if 'credentials' not in session:
        return redirect('authorize')
    
    # Load creds from session
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials']
    )

    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', credentials=credentials
    )

    subscriptions_list = youtube.subscriptions().list(
        part='id, snippet',
        mine=True,
        order="unread",
        pageToken="CAUQAA"

    ).execute()

    return jsonify(**subscriptions_list)

# run server
if __name__=="__main__":
    app.run(debug=True)