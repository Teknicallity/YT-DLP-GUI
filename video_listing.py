import io
import os.path
from os import startfile
from PIL import Image
import cloudscraper

import yt_download
import yt_search


# replace the youtube api with ytdlp
# https://github.com/yt-dlp/yt-dlp#extracting-information

class VideoListing:

    def __init__(self, id: str, title: str = None, downloaded: bool = False):
        self.title = title
        self.id = id
        self.channel = None
        self.thumbnail_url = None
        self.thumbnail_data = None
        self.runtime = None
        self.file_path = None
        self.video_file_name = None
        self.is_downloaded = downloaded
        self.info = yt_search.get_video_info_from_id(id)

        self.fill_info()

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
        self.title = self.info['title']
        self.channel = self.info['channelTitle']
        self.thumbnail_url = self.fill_thumbnail_url()

        self.thumbnail_data = self.fill_thumbnail_data()

    def fill_thumbnail_url(self):
        """
        tries to get the standard resolution url, or the next highest resolution
        :return:
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

    def fill_thumbnail_data(self):
        """
        https://stackoverflow.com/questions/69578469/pysimplegui-displaying-a-url-jpg
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

    def download(self, download_folder: str):
        self.file_path = download_folder
        yt_download.download_video_listing(self, download_folder)
        self.is_downloaded = True
        self.video_file_name = self.title + '.mp4'

    def play_video(self):
        path = os.path.join(self.file_path , self.video_file_name)
        print("Download Path:", path)
        startfile(path)
