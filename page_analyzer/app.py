from flask import (
    get_flashed_messages,
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv
import os
import psycopg2
import validators
from page_analyzer.repository import DataBase
from bs4 import BeautifulSoup

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
db = DataBase(conn)
db.initialize_database()


@app.route("/")
def index():
    return render_template("index.html", url="")


@app.post("/")
def add_url():
    url = request.form.get("url", "").strip()

    if not validators.url(url) and len(url) < 255:  # check is valid or not
        flash("Некорректный URL", "danger")
        return render_template("index.html")

    parsed_url = urlparse(url)  # normalize url
    normalized_url = urlunparse(
        (parsed_url.scheme, parsed_url.hostname, "", "", "", "")
    )

    existing_url = db.get_by_url(normalized_url)  # cheks if excist in db or not

    if existing_url:  # if yes --> return flash-message and redirect on this url's page
        flash("Этот URL уже существует!", "info")
        return redirect(url_for("url_show", id=existing_url["id"]))

    # if not exsist -->
    new_url = db.add(normalized_url)  # add into db normolized url

    flash("Страница успешно добавлена", "success")
    return redirect(url_for("url_show", id=new_url["id"]))


@app.route("/urls/<int:id>")  #
def url_show(id):
    url = db.get(id)
    checks = db.get_checks_by_url_id(id)
    return render_template("one_url.html", url=url, checks=checks)


@app.route("/urls")
def all_urls():
    urls = db.get_all_urls_with_last_check()
    return render_template("all_urls.html", urls=urls)


@app.post("/urls/<int:id>/checks")
def url_checks(id):
    url = db.get(id)
    if not url:
        flash("URL не найден", "danger")
        return redirect(url_for("all_urls"))

    try:
        r = requests.get(url["name"])
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        h1 = soup.h1.string if soup.h1.string else None
        title = soup.title.string if soup.title.string else None
        status_code = r.status_code
        created_at = datetime.now()
        meta_tag = soup.find("meta", attrs={"name": "description"})

        if meta_tag and "content" in meta_tag.attrs:
            description = meta_tag["content"]
        else:
            description = None

        db.add_check(
            url_id=id,
            status_code=status_code,
            h1=h1,
            title=title,
            description=description,
            created_at=created_at,
        )
        flash("Страница успешно проверена", "succuss")
    except Exception as e:
        flash(f"Произошла ошибка при проверке: {e}", "danger")

    return redirect(url_for("url_show", id=id))
