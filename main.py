import yt_dlp


coub_link = 'https://coub.com/view/38jy5l'

ydl_opts = {
    'format': 'html5-video-higher,html5-audio-high',
    'paths': {'home': './temp'},
    'keepvideo': True,
    'outtmpl': {
        'default': "%(title)s_[%(uploader)s]_[%(id)s].%(ext)s"
    },
}


class Downloader:
    """
    Download coubs separately (don't merge):
        - best audio
        - best video
    """

    @classmethod
    def download(cls, url: str, options: dict = {}):
        if options:
            with yt_dlp.YoutubeDL(options) as ydl:
                error_code = ydl.download(url)


class Prepare:
    """
    We need to hash filenames
    and encode them back for the sake of system side execution
    """

    @classmethod
    def filenames(cls):
        pass

    @classmethod
    def decode_filenames(cls):
        pass

    @classmethod
    def decode_filename(cls):
        pass

    @classmethod
    def encode_filenames(cls):
        pass

    @classmethod
    def encode_filename(cls):
        pass


class Coubify:
    """
    - Encode back
    - Merge audio+video by looping video by audio length
    """




Downloader.download(coub_link, ydl_opts)
filenames = Prepare.filenames()
# Prepare.
