from flask import request, jsonify, session, url_for, redirect, Blueprint

from app.main.utils.youtube_api.subscriptions_manager import subscriptions_manager

subscription = Blueprint('subscription', __name__)

# @subscription.route('/subscription', methods=['GET'])
# def get_first_page_subscriptions():
#     # Check if user is logged in
#     if 'credentials' not in session:
#         return redirect('authorize')
    
#     subscriptions_list = request_subscriptions(session['credentials'])
    
#     return jsonify(**subscriptions_list)

@subscription.route('/subscription', methods=['GET'])
@subscription.route('/subscription/<page_token>', methods=['GET'])
def get_page_subscriptions(page_token = ''):
    # Check if user is logged in
    if 'credentials' not in session:
        return redirect('authorize')
    
    subscriptions_list = subscriptions_manager.request_subscriptions(page_token)
    
    return jsonify(**subscriptions_list)

@subscription.route('/subscription/<subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    # Check if user is logged in
    if 'credentials' not in session:
        return redirect('authorize')
    
    subscriptions_manager.delete_subscription(subscription_id)