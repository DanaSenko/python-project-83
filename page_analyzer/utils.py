from urllib.parse import urlparse
import validators


def normalize_url(url):
    parts = urlparse(url)
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}"


def validate(url):
    if not url:
        return "Поле обязательно для заполнения"
    if not validators.url(url):
        return "Некорректный URL"
    if len(url) > 255:
        return "Длина URL превышает разрешенную"
    return None
