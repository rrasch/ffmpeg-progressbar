from flask import Flask, request, g, render_template, jsonify
import json
import logging
import re
import redis

app = Flask(__name__)
db = redis.Redis(decode_responses=True)

# def get_db():
#     if "db" not in g:
#         g.db = redis.Redis(decode_responses=True)
#     return g.db


@app.teardown_appcontext
def close_db(e=None):
    # db = g.pop("db", None)
    if db is not None:
        db.close()


# from flask_redis import FlaskRedis
# redis = FlaskRedis()
#
# def create_app():
#     app = Flask(__name__)
#     redis.init_app(app, url='redis://localhost:6379/0')
#     return app


@app.route("/update/<video>/<duration>", methods=["POST"])
def update_progress(video, duration):
    # db = get_db()
    db.hset(video, "duration", duration)
    for chunk in request.stream:
        # print(chunk.decode("utf-8"))
        match = re.match("^frame=(\d+)$", chunk.decode())
        if match:
            frame = int(match.group(1))
            logging.debug(f"frame: {frame}")
            db.hset(video, "frame", frame)
            db.expire(video, 60)
    return "Chunks printed successfully"


def progress_dict():
    progress = {}
    for video in db.scan_iter("*"):
        logging.debug(f"video: {video}")
        data = db.hgetall(video)
        data["percent"] = int(int(data["frame"]) / int(data["duration"]) * 100)
        progress[video] = data
    return progress


@app.route("/")
def index():
    return render_template("index.html", progress=progress_dict())


@app.route("/data")
def progress():
    return jsonify(progress=progress_dict())


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(port=5000, debug=True)
    # app.run(port=5443, ssl_context="adhoc", debug=True)
