from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)
from .parser import extract_page_data
from .utils import normalize_url, validate
from dotenv import load_dotenv
import os
from .repository import DataBase, get_db, close_db
import requests
from datetime import datetime


load_dotenv()

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

"""close connection after each request"""
app.teardown_appcontext(close_db)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


@app.route("/")
def index():
    return render_template("index.html", url="")


@app.post("/urls")
def add_url():
    url = request.form.get("url", "").strip()
    error_message = validate(url)
    if error_message:
        flash(error_message, "danger")
        return render_template("index.html"), 422

    db = DataBase(get_db(DATABASE_URL))
    normalized_url = normalize_url(url)
    existing_url = db.get_by_url(normalized_url)

    if existing_url:
        flash("Страница уже существует", "info")
        return redirect(url_for("url_show", id=existing_url.id))

    new_url_id = db.add_url(normalized_url)

    flash("Страница успешно добавлена", "success")
    return redirect(url_for("url_show", id=new_url_id))


@app.route("/urls/<int:id>")
def url_show(id):
    db = DataBase(get_db(DATABASE_URL))
    url = db.get_url_by_id(id)
    checks = db.get_checks_by_url_id(id)
    return render_template("one_url.html", url=url, checks=checks)


@app.route("/urls")
def all_urls():
    db = DataBase(get_db(DATABASE_URL))
    urls = db.get_all_urls_with_last_check()
    return render_template("all_urls.html", urls=urls)


@app.post("/urls/<int:id>/checks")
def url_checks(id):
    db = DataBase(get_db(DATABASE_URL))
    url = db.get_url_by_id(id)
    if not url:
        flash("URL не найден", "danger")
        return redirect(url_for("all_urls"))

    try:
        response = requests.get(url["name"])
        page_data = extract_page_data(response)
        created_at = datetime.today().date()

        db.add_check_of_url(
            url_id=id,
            status_code=page_data['status_code'],
            h1=page_data["h1"],
            title=page_data["title"],
            description=page_data["meta_description"],
            created_at=created_at,
        )
        flash("Страница успешно проверена", "success")
    except Exception:
        flash("Произошла ошибка при проверке", "danger")

    return redirect(url_for("url_show", id=id))
