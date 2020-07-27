import io
import os
from datetime import datetime

import dateparser
import google.auth
import httpx
from babel.dates import format_timedelta
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, request, send_file
from google.cloud import storage
from logger import getJSONLogger

app = Flask(__name__)
logger = getJSONLogger("testLog")

client = storage.Client()
_, project = google.auth.default()
bucket = client.bucket(os.environ.get("BADGE_BUCKET", f"{project}-media"))
MIMETYPE = "image/svg+xml"
SERVICE_SUB = "_SERVICE"  # _SERVICE_NAME


def service_badge_uri(service):
    return f"service/{service}.svg"


@app.route("/service/<name>.svg")
def service_badge(name):
    image = get_image(service_badge_uri(name))
    return send_file(image, mimetype=MIMETYPE)


def tag_badge_uri(tag):
    return f"tag/{tag}.svg"


@app.route("/tag/<name>.svg")
def tag_badge(name):
    image = get_image(tag_badge_uri(name))
    return send_file(image, mimetype=MIMETYPE)


def get_image(ident):
    blob = bucket.blob(ident)
    data = blob.download_as_string()
    image = io.BytesIO()
    image.write(data)
    image.seek(0)
    return image


@app.route("/receive", methods=["POST", "GET"])
def receive():
    if request.method == "GET":
        return "HTTP 405 I do not respond to GET", 405

    data = request.json
    if not data:
        return "No data received", 400

    logger.debug(data)

    def get_sub(data, key, default):
        if "substitutions" in data.keys():
            if key in data["substitutions"]:
                return data["substitutions"][key]
        return default

    def store_badge(location, label, message, color):
        label = label.replace("-", "_")
        badge_url = (
            f"https://img.shields.io/badge/{label}-{message}-{color}"
            "?style=flat-square&logo=google-cloud&logoColor=white"
        )
        logger.info(f"Badge URL: {badge_url}")
        badge_blob = httpx.get(badge_url).content
        blob = storage.Blob(location, bucket=bucket)
        blob.upload_from_string(badge_blob, content_type=MIMETYPE)
        logger.info(f"Badge uploaded to {blob.bucket.name} -- {blob.name}")

    message = get_sub(data, "SHORT_SHA", "manual")
    color = "success" if data["status"] == "SUCCESS" else "critical"
    if "tags" in data.keys():
        tags = data["tags"]
        for t in tags:
            location = tag_badge_uri(t)
            store_badge(location, t, message, color)
    service = get_sub(data, SERVICE_SUB, "service")
    location = service_badge_uri(service)
    store_badge(location, t, message, color)

    return "Success", 201


# ADMIN
@app.route("/badges")
def badge_list():
    def relative_time(dstr):
        if not dstr:
            return "(no data)"
        delta = dateparser.parse("now Z") - dateparser.parse(
            dstr, settings={"TIMEZONE": "Z"}
        )
        return f"{format_timedelta(delta)} ago"

    blobs = list(bucket.list_blobs())
    data = []
    for b in blobs:
        svg = b.download_as_string()
        text = ": ".join([x.text for x in bs(svg, "html.parser").find_all("text")])
        data.append(
            {
                "name": b.name,
                "updated": b.updated,
                "relative": relative_time(str(b.updated)),
                "data": text,
            }
        )
    return render_template("badge.html", data=data)


@app.route("/")
def hi():
    return "HTTP 200 Beep Boop"


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
