class VideoListing:

    def __init__(self, id: str, title: str = None, channel: str = None, runtime: str = None,
                 thumbnail_path: str = None, video_path: str = None, downloaded: bool = False):
        self.title = title
        self.channel = channel
        self.runtime = runtime
        self.id = id
        self.thumbnail_path = thumbnail_path
        self.video_name = video_path
        self.downloaded = downloaded

    def __str__(self):
        return self.id

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
