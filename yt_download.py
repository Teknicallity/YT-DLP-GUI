import yt_dlp


def download_video_listing(video, path: str):
    # r'\/:*?"<>|'
    video_ext: str = '/%(title)s.%(ext)s'
    # p = ''.join((path, video_ext))

    p = str(path) + video_ext
    ydl_opts = {
        'outtmpl': p,
        'windowsfilenames': True
        # 'restrictfilenames': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download('www.youtube.com/watch?v=' + video.id)


def get_video_file_name(video, path: str):
    video_ext: str = '/%(title)s.%(ext)s'
    p = str(path) + video_ext
    ydl_opts = {
        'outtmpl': p,
        'windowsfilenames': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info('https://www.youtube.com/watch?v=' + video.id, download=False)
        video_file_name = "{0}.{1}".format((meta['title']), 'mp4')
        print("video file name:", video_file_name)
        return video_file_name

