import os

import google_auth_oauthlib
import google.oauth2.credentials

import googleapiclient.discovery


basedir = os.path.abspath(os.path.dirname(__file__))
client_secret_file_path = os.path.join(basedir, 'client_secret.json')

def get_authorization_url(redirect_url):


    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_file_path, 
        [
            'https://www.googleapis.com/auth/youtube.force-ssl',
            'https://www.googleapis.com/auth/youtubepartner',
            'https://www.googleapis.com/auth/youtube'
        ]
    )

    flow.redirect_uri = redirect_url

    return flow.authorization_url(
        include_granted_scopes='true',
        state="statevalue",
        prompt='consent',

    )

def exchange_code_for_credentials(redirect_url, authorization_response):

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secret_file_path,
        [
            'https://www.googleapis.com/auth/youtube.force-ssl',
        ]
    )

    flow.redirect_uri = redirect_url
    
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
