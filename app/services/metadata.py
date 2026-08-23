from app.utils.urls import identify_platform
import yt_dlp

def get_metadata(url):
    platform = identify_platform(url)

    if platform is None:
        return None

    if platform =="youtube":
        ydl_opts =  {
            "quiet":True,
            "no_warnings":True,
            "skip_download":True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url,download=False)

        return {
                "url":url,
                "platform":platform,
                "title":info.get("title"),
                "thumbnail":info.get("thumbnail"),
            }

    return {
        "url":url,
        "platform":platform,
        "title":None,
        "thumbnail":None
    }