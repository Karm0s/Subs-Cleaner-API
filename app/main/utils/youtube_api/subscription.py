import google_auth_oauthlib.flow
import google.oauth2.credentials

import googleapiclient.discovery


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

    return {
        'items':items,
        'next_page_token':subscriptions_list['nextPageToken'],
        'pageInfo': subscriptions_list['pageInfo']
    }
