from flask import Flask, request, g
import logging
import re
import redis

app = Flask(__name__)
# db = redis.Redis(decode_responses=True)

def get_db():
    if "db" not in g:
        g.db = redis.Redis(decode_responses=True)
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# from flask_redis import FlaskRedis
# redis = FlaskRedis()
# 
# def create_app():
#     app = Flask(__name__)
#     redis.init_app(app, url='redis://localhost:6379/0')
#     return app


@app.route("/progress/<vid>/<bitrate>", methods=["POST"])
def print_chunks(vid, bitrate):
    db = get_db()
    for chunk in request.stream:
        # print(chunk.decode("utf-8"))
        match = re.match("^frame=(\d+)$", chunk.decode())
        if match:
            frame = int(match.group(1))
            logging.debug(f"frame: {frame}")
            db.set(vid, frame)
    return "Chunks printed successfully"


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(debug=True)

