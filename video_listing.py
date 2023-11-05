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
        return self.url_link

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.url_link):
            raise StopIteration
        else:
            result = self.url_link[self.index]
            self.index += 1
            return result

    def lower(self):
        return self.__str__().lower()
