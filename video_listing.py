
class VideoListing:

    def __init__(self, url_link: str, title: str = None, channel: str = None, runtime: str = None,
                 thumbnail_path: str = None, video_path: str = None, downloaded: bool = False):
        self.title = title
        self.channel = channel
        self.runtime = runtime
        self.url_link = url_link
        self.thumbnail_path = thumbnail_path
        self.video_name = video_path
        self.downloaded = downloaded

    def __str__(self):
        return self.title

