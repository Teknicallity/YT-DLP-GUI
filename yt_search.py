from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = 'AIzaSyCxmI523SrQTeCq2ZQFAZ0eoVfEDS-gpxk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

'''
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results
    ).execute()
'''


def get_video_info_from_id(video_id) -> dict:
    """

    :param video_id: end of the full youtube url
    :return: dictionary of the video info
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    video_response = youtube.videos().list(id=video_id, part='snippet').execute()

    if 'items' in video_response:
        video_info = video_response['items'][0]['snippet']  # returns dictionary
        return video_info
    else:
        return None
