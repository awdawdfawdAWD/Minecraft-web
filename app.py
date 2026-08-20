from flask import Flask, render_template, redirect, jsonify
import os

app = Flask(__name__)

CLIENT_URL = "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/unkk-62.0.0.20260820.085414.jar"
FABRIC_API_URL = "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/fabric-api-0.156.0+26.2.jar"

@app.route("/")
def index():
    return render_template("index.html", client_url=CLIENT_URL, fabric_url=FABRIC_API_URL)

@app.route("/api/download/client")
def download_client():
    return redirect(CLIENT_URL)

@app.route("/api/download/fabric")
def download_fabric():
    return redirect(FABRIC_API_URL)

@app.route("/api/info")
def api_info():
    return jsonify({
        "name": "unkk Minecraft Client",
        "version": "62.0.0",
        "downloads": {
            "client": CLIENT_URL,
            "fabric_api": FABRIC_API_URL
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
