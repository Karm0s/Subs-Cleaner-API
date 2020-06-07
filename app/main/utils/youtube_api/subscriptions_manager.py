import google_auth_oauthlib.flow
import google.oauth2.credentials

import googleapiclient.discovery
from googleapiclient.errors import HttpError

import json


class YoutubeSubscriptionsManager():
    def __init__(self):
        self.subscriptions = None
    
    def build(self, credentials):
        credentials = google.oauth2.credentials.Credentials(
        **credentials
        )

        self.subscriptions = googleapiclient.discovery.build(
            'youtube', 'v3', credentials=credentials
        ).subscriptions()

    def request_subscriptions(self, page_token = ''):
        
        try:
            subscriptions_list = self.subscriptions.list(
                part='id, snippet',
                mine=True,
                order="unread",
                maxResults=50,
                pageToken=page_token

            ).execute()
            status = 200
        except HttpError as error:
            if error.resp.get('content-type', '').startswith('application/json'):
                reason = json.loads(error.content).get('error').get('errors')[0].get('reason')    
            status = error.resp.status
            return {
                'status': status,
                'error': reason 
            }
        items = []

        for item in subscriptions_list['items']:
            new_item = {
                'id':item['id'],
                'thumbnails': item['snippet']['thumbnails'],
                'title': item['snippet']['title']
            }
            items.append(new_item)

        response = {
            'status': status,
            'items':items,
            'next_page_token':subscriptions_list['nextPageToken'],
            'pageInfo': subscriptions_list['pageInfo']
        }

        if 'prevPageToken' in subscriptions_list:
            response['previous_page_token'] = subscriptions_list['prevPageToken']

        return response

    def delete_subscription(self, subscription_id):
        try:
            response = self.subscriptions.delete(
                id = subscription_id
            ).execute()
            status = 200
        except HttpError as error:
            if error.resp.get('content-type', '').startswith('application/json'):
                reason = json.loads(error.content).get('error').get('errors')[0].get('reason')    
            status = error.resp.status
            return {
                'status': status,
                'error': reason 
            }

        return {
            'status': status,
            'message': 'Subscription deleted'
        }

subscriptions_manager = YoutubeSubscriptionsManager()


def request_subscriptions(session_credentials, page_token = ''):
    credentials = google.oauth2.credentials.Credentials(
        **session_credentials
    )

    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', credentials=credentials
    )

    subscriptions_list = youtube.subscriptions().list(
        part='id, snippet',
        mine=True,
        order="unread",
        maxResults=50,
        pageToken=page_token

    ).execute()

    items = []

    for item in subscriptions_list['items']:
        new_item = {
            'id':item['id'],
            'thumbnails': item['snippet']['thumbnails'],
            'title': item['snippet']['title']
        }
        items.append(new_item)

    response = {
        'items':items,
        'next_page_token':subscriptions_list['nextPageToken'],
        'pageInfo': subscriptions_list['pageInfo']
    }

    if 'prevPageToken' in subscriptions_list:
        response['previous_page_token'] = subscriptions_list['prevPageToken']

    return response 


