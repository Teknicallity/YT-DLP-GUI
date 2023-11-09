import yt_dlp


def download_video_listing(video):
    ydl_opts = {
        'outtmpl': './videos/%(title)s.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download('www.youtube.com/watch?v=' + video.id)
