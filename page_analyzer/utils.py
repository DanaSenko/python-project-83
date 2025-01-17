from urllib.parse import urlparse
import validators


def normalize_url(url):
    parts = urlparse(url)
    return f"{parts.scheme}://{parts.netloc}".lower()


def validate(url):
    if not validators.url(url) or len(url) > 255:
        return False
    return True
