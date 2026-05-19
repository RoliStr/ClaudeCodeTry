"""Multi-tool portal.

Landing page lists every registered tool; each tool is a Flask Blueprint
mounted under /tools/<slug>. Add new tools via tools/__init__.py.
"""
import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

from tools import TOOLS, BLUEPRINTS

load_dotenv()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB upload limit

for bp in BLUEPRINTS:
    app.register_blueprint(bp)


@app.route("/")
def portal():
    return render_template("portal.html", tools=TOOLS)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": os.environ.get("APP_VERSION", "dev")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
