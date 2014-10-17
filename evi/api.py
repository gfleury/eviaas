from flask import Flask

import os


app = Flask(__name__)
app.debug = os.environ.get("API_DEBUG", "0") in ("True", "true", "1")


@app.route("/resources", methods=["POST"])
def add_instance():
    return "", 201


@app.route("/resources/<name>", methods=["DELETE"])
def remove_instance(name):
    return "", 200


@app.route("/resources/<name>/hostname/<host>", methods=["DELETE"])
def unbind(name, host):
    return "", 200


@app.route("/resources/<name>", methods=["POST"])
def bind(name):
    return os.environ.get("EVI_ENVIRONS", "{}"), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
