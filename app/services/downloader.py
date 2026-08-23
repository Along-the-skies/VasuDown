from app.utils.urls import identify_platform
from app.platforms.youtube import download_youtube_video as download_youtube

def download_media(url):
    platform = identify_platform(url)

    if platform =="youtube":
        return download_youtube(url)
    elif platform == "instagram":
        #return download_instagram(url)
        pass
    elif platform == "facebook":
        #return download_facebook(url)
        pass

    return None