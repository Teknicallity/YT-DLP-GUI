import io
import os.path
from os import startfile, remove
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

    def download(self, download_folder: str):
        """

        :param download_folder: The folder which the video should be downloaded to
        """
        self.file_path = download_folder
        yt_download.download_video_listing(self, download_folder)
        self.is_downloaded = True
        self.video_file_name = self.title + '.mp4'

    def play_video(self):
        """
        Uses os.startfile to play the video with the system's default video player
        """
        raw_path = os.path.join(self.file_path , self.video_file_name)
        path = os.path.normpath(raw_path)
        print("Download Path:", path)
        try:
            os.startfile(path)
        except OSError as e:
            print(f"Error playing video: {e}")

    def delete_video(self):
        """
        Uses os.remove to delete the video from the filesystem
        """
        raw_path = os.path.join(self.file_path, self.video_file_name)
        path = os.path.normpath(raw_path)
        print("Video Deleted:", path)
        try:
            os.remove(path)
        except OSError as e:
            print(f"Error deleting video: {e}")
