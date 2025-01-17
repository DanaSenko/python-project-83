from bs4 import BeautifulSoup


def parse_html(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    h1_tag = soup.h1.get_text(strip=True) if soup.h1 else ""

    title_tag = soup.title.get_text(strip=True) if soup.title else ""

    meta_tag = soup.find("meta", attrs={"name": "description"})
    description = (
        meta_tag["content"].strip()
        if meta_tag and "content" in meta_tag.attrs
        else ""
    )

    return {"title": title_tag, "h1": h1_tag, "description": description}
