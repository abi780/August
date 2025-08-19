from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    version = os.environ.get("VERSION", "v2")
    return f"Hello from Flask Demo-2 Version: {version}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

