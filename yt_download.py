import yt_dlp


def download_video_listing(video, path: str):
    video_ext: str = '/%(title)s.%(ext)s'
    # p = ''.join((path, video_ext))

    p = str(path) + video_ext
    ydl_opts = {
        'outtmpl': p
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download('www.youtube.com/watch?v=' + video.id)
