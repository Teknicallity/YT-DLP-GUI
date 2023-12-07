"""
Copyright (c) 2023, Joshua Sheputa
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
"""
import io
import os
import sys
import subprocess

import yt_dlp
from PIL import Image
import cloudscraper
import yt_search


# replace the youtube api with ytdlp
# https://github.com/yt-dlp/yt-dlp#extracting-information

class VideoListing:

    def __init__(self, id: str):
        self.title: str = ''
        self.id = id
        self.channel = None
        self.thumbnail_url = None
        self.thumbnail_data = None  # the thumbnail converted to png data in io bytes
        self.file_directory = None
        self.is_downloaded = False
        self.info = yt_search.get_video_info_from_id(id)  # dictionary pulled from yt API

        self.fill_info()
        self.video_file_name = clean_title(self.title)  # filename without extention

    def __str__(self):
        return self.title

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.id):
            raise StopIteration
        else:
            result = self.id[self.index]
            self.index += 1
            return result

    def lower(self):
        return self.__str__().lower()

    def fill_info(self):
        """
        Fills the video object's values based on the video info dictionary
        """
        self.title = self.info['title']
        self.channel = self.info['channelTitle']
        self.thumbnail_url = self._fill_thumbnail_url()

        self.thumbnail_data = self._fill_thumbnail_data()

    def _fill_thumbnail_url(self):
        """
        Checks if the video info contains a standard resolution thumbnail, and if not, gets the next highest resolution.
        :return: The url of the highest resolution thumbnail up to standard
        """
        preferred_resolutions = ['standard', 'high', 'medium', 'default']
        for resolution in preferred_resolutions:
            if resolution in self.info['thumbnails']:
                return self.info['thumbnails'][resolution]['url']

    # def get_base64_from_png(self):
    #     """
    #     https://github.com/PySimpleGUI/PySimpleGUI/issues/6063#issuecomment-1328260218
    #     :return: base64 encoded image
    #     """
    #     print(self.thumbnail_url)
    #     return base64.b64encode(urllib.request.urlopen(self.thumbnail_url).read())

    def _fill_thumbnail_data(self):
        """
        Downloads an image from a given URL, converts it to PNG format, and returns the PNG data.

        This function utilizes the cloudscraper library to bypass anti-scraping measures on websites.
        It fetches the image from the specified thumbnail URL, converts the image data from JPG to PIL Image,
        and then saves it in PNG format. The resulting PNG data is returned.
        Source: https://stackoverflow.com/questions/69578469/pysimplegui-displaying-a-url-jpg
        :return:
        """
        jpg_data = (
            cloudscraper.create_scraper(
                browser={"browser": "firefox", "platform": "windows", "mobile": False}
            )
            .get(self.thumbnail_url)
            .content
        )

        pil_image = Image.open(io.BytesIO(jpg_data))
        png_bio = io.BytesIO()
        pil_image.save(png_bio, format="PNG")
        return png_bio.getvalue()

    def download_to(self, download_folder: str):
        """Sets up and calls the downloader

        :param download_folder: The folder which the video should be downloaded to
        """
        self.file_directory = download_folder
        self.download_video_listing()
        self.is_downloaded = True
        # self.video_file_name = self.title + '.mp4'

    def play_video(self):
        """Plays the video with the system's default video player

        Uses os.startfile (windows) or opener subprocess (unix) to open the video
        """
        path = self._get_video_file_path()
        print("Download Path:", path)
        try:
            if sys.platform == "win32":
                os.startfile(path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, path])
        except OSError as e:
            print(f"Error playing video: {e}")

    def delete_video(self):
        """Deletes the video from the filesystem

        Gets the file path for the video, then removes it barring exceptions
        """
        path = self._get_video_file_path()
        print("Video Deleted:", path)
        try:
            os.remove(path)
        except OSError as e:
            print(f"Error deleting video: {e}")

    def _get_video_file_path(self) -> str:
        """Generates the proper video file path for the host operating system

        :return: string
            The full path to the video
        """
        raw_path = os.path.join(self.file_directory, self.video_file_name + '.mp4')
        return os.path.normpath(raw_path)

    def download_video_listing(self):
        """Downloads the video using yt-dlp

        Gets the filename prepped to be passed to yt-dlp, then combines it with the intended download directory.
        Calls yt-dlp with the specified output
        :param self:
        """
        # not allowed windows symbols: \/:*?"<>|
        video_ext: str = '/' + self.video_file_name + '.%(ext)s'
        # p = ''.join((path, video_ext))

        p = str(self.file_directory) + video_ext
        ydl_opts = {
            'outtmpl': p,
            'windowsfilenames': True
            # 'restrictfilenames': True
        }
        # follows the options set
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download('www.youtube.com/watch?v=' + self.id)


def clean_title(raw_title: str) -> str:
    """Cleans a string by getting rid of illegal windows filename characters

    :param raw_title: the string to be sanitized
    :return: the sanitized string
    """
    # \/:*?"<>|
    invalid_chars = ['\\', '/', ':', '*', '?', '<', '>', '|']
    new_string = ''
    for char in raw_title:
        if char not in invalid_chars:
            new_string += char

    return new_string
