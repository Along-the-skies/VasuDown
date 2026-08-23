from urllib.parse import urlparse


def is_valid_url(url):
    parsed = urlparse(url)

    return (
        parsed.scheme == "https"
        and bool(parsed.hostname)
    )


def identify_platform(url):
    parsed = urlparse(url)
    domain = parsed.hostname.lower()

    if domain in ("youtube.com", "www.youtube.com", "youtu.be"):
        return "youtube"

    elif domain in ("instagram.com", "www.instagram.com"):
        return "instagram"

    elif domain in ("facebook.com", "www.facebook.com"):
        return "facebook"

    return None