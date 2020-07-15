import io
from flask import Flask, request, send_file
import os
from google.cloud import storage
import google.auth
from datetime import datetime
import httpx

app = Flask(__name__)
client = storage.Client()
_, project = google.auth.default()
bucket = client.bucket(os.environ.get("BADGE_BUCKET", f"{project}-media"))

@app.route("/")
def hi():
    return "HTTP 200 Beep Boop"

def service_badge_uri(service):
    return f"badge/{service}.svg"

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
    label = service.replace("-","--")
    commit = get_sub(data, "COMMIT_SHA", "manual")
    status = "success" if data["status"] == "SUCCESS" else "critical"

    badge_url = (f"https://img.shields.io/badge/{label}-{commit}-{status}"
                   "?style=flat-square&logo=google-cloud&logoColor=white")
    app.logger.info(f"Badge URL: {badge_url}")
    badge_blob = httpx.get(badge_url).content

    blob = storage.Blob(service_badge_uri(service), bucket=bucket)
    blob.upload_from_string(badge_blob,
            content_type=service_badge_mimetype())

    app.logger.info(f"Badge uploaded to {blob.bucket.name} -- {blob.name}")

    return "Success", 201

@app.route("/service/<name>/badge.svg")
def service_badge(name):
    image = get_image(service_badge_uri(name))

    return send_file(image, mimetype=service_badge_mimetype())


def get_image(ident):
    blob = bucket.blob(ident)
    data = blob.download_as_string()
    image = io.BytesIO()
    image.write(data)
    image.seek(0)
    return image


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
