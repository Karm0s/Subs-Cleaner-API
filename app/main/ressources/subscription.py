from flask import request, jsonify, session, url_for, redirect, Blueprint

from app.main.utils.youtube_api.subscriptions_manager import subscriptions_manager

subscription = Blueprint('subscription', __name__)

@subscription.route('/subscription', methods=['GET'])
@subscription.route('/subscription/<page_token>', methods=['GET'])
def get_page_subscriptions(page_token = ''):
    # Check if user is logged in
    if 'credentials' not in session:
        return redirect('authorize')
    
    response = subscriptions_manager.request_subscriptions(page_token)
    
    return jsonify(**response)

@subscription.route('/subscription/<subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    # Check if user is logged in
    if 'credentials' not in session:
        return redirect('authorize')
    
    response = subscriptions_manager.delete_subscription(subscription_id)

    return jsonify(**response)