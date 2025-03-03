from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from page_analyzer.db import get_db, close_db
from page_analyzer.parser import parse_html
from page_analyzer.utils import normalize_url, validate
from dotenv import load_dotenv
import os
import psycopg2
from page_analyzer.repository import DataBase
import requests
from datetime import datetime


load_dotenv()
app = Flask(__name__)
with app.app_context():
    db = DataBase(get_db())
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html", url="")


@app.post("/")
def add_url():
    url = request.form.get("url", "").strip()

    if not validate(url):
        flash("Некорректный URL", "danger")
        return render_template("index.html")

    normalized_url = normalize_url(url)
    existing_url = db.get_by_url(normalized_url)

    if existing_url:
        flash("Страница уже существует", "info")
        return redirect(url_for("url_show", id=existing_url["id"]))

    new_url_id = db.add(normalized_url)

    flash("Страница успешно добавлена", "success")
    return redirect(url_for("url_show", id=new_url_id))


@app.route("/urls/<int:id>")
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
        req = requests.get(url["name"])
        req.raise_for_status()
        html = req.text
        parsed_data = parse_html(html)
        created_at = datetime.today().date()

        db.add_check(
            url_id=id,
            status_code=req.status_code,
            h1=parsed_data["h1"],
            title=parsed_data["title"],
            description=parsed_data["description"],
            created_at=created_at,
        )
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")

    return redirect(url_for("url_show", id=id))
