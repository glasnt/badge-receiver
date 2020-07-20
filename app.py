import io
import logging
import os
from datetime import datetime

import dateparser
import google.auth
import httpx
from babel.dates import format_timedelta
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, request, send_file
from google.cloud import storage

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

client = storage.Client()
_, project = google.auth.default()
bucket = client.bucket(os.environ.get("BADGE_BUCKET", f"{project}-media"))


# media bucket storage location (doesn't have to be nice)
def service_badge_uri(service):
    return f"badge/{service}.svg"


# nice URL
@app.route("/badge/<name>.svg")
def service_badge(name):
    image = get_image(service_badge_uri(name))

    return send_file(image, mimetype=service_badge_mimetype())


def relative_time(dstr):
    if not dstr:
        return "(no data)"
    delta = dateparser.parse("now Z") - dateparser.parse(
        dstr, settings={"TIMEZONE": "Z"}
    )
    return f"{format_timedelta(delta)} ago"


def get_image(ident):
    blob = bucket.blob(ident)
    data = blob.download_as_string()
    image = io.BytesIO()
    image.write(data)
    image.seek(0)
    return image


def service_badge_mimetype():
    return "image/svg+xml"


def get_sub(data, key, default):
    if "substitutions" in data.keys():
        if key in data["substitutions"]:
            return data["substitutions"][key]
    return default


@app.route("/receive", methods=["POST", "GET"])
def receive():
    if request.method == "GET":
        return "HTTP 405 I do not respond to GET", 405

    data = request.json
    if not data:
        return "No data received", 400

    # TODO: this presumes settings not all cloudbuild.yaml's have
    # COULD use a step parser to see what the "gcloud run deploy X" value is
    # or query back from the trigger ID
    service = get_sub(data, "_SERVICE", "service")
    label = service.replace("-", "--")
    commit = get_sub(data, "SHORT_SHA", "manual")
    status = "success" if data["status"] == "SUCCESS" else "critical"

    badge_url = (
        f"https://img.shields.io/badge/{label}-{commit}-{status}"
        "?style=flat-square&logo=google-cloud&logoColor=white"
    )
    app.logger.info(f"Badge URL: {badge_url}")
    badge_blob = httpx.get(badge_url).content

    blob = storage.Blob(service_badge_uri(service), bucket=bucket)
    blob.upload_from_string(badge_blob, content_type=service_badge_mimetype())

    app.logger.info(f"Badge uploaded to {blob.bucket.name} -- {blob.name}")

    return "Success", 201


@app.route("/badge")
def badge_list():
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
