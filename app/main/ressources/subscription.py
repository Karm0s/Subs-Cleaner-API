from flask import request, jsonify, session, url_for, redirect, Blueprint

from app.main.utils.youtube_api.subscription import request_subscriptions

subscription = Blueprint('subscription', __name__)

@subscription.route('/subscription', methods=['GET'])
def get_first_page_subscriptions():
    # Check if user is logged in
    if 'credentials' not in session:
        return redirect('authorize')
    
    subscriptions_list = request_subscriptions(session['credentials'])
    print(subscriptions_list)
    
    return jsonify(**subscriptions_list)


@subscription.route('/subscription/<page_token>', methods=['GET'])
def get_page_subscriptions(page_token):
    # Check if user is logged in
    if 'credentials' not in session:
        return redirect('authorize')
    
    subscriptions_list = request_subscriptions(session['credentials'], page_token)
    
    response = {
        'items':subscriptions_list['items'],
        'next_page_token':subscriptions_list['nextPageToken'],
        'previous_page_token': subscriptions_list['prevPageToken'],
        'pageInfo': subscriptions_list['pageInfo']
    }
    return jsonify(**response)
