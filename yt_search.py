"""
Copyright (c) 2023, Joshua Sheputa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import configparser


def parse_config() -> str:
    config_object = configparser.ConfigParser()
    with open("config.ini", "r") as file_object:
        config_object.read_file(file_object)
        return config_object.get("ytapi", "apikey")


DEVELOPER_API_KEY = parse_config()
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_video_info_from_id(video_id) -> dict | None:
    """Grabs the video information from the Youtube API

    :param video_id: end of the full youtube url
    :return: dictionary of the video info
    """
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_API_KEY)

    video_response = youtube.videos().list(id=video_id, part='snippet').execute()

    if 'items' in video_response:
        video_info = video_response['items'][0]['snippet']  # returns dictionary
        return video_info
    else:
        return None
