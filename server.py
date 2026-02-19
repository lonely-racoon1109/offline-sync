from flask import Flask, request, jsonify, redirect, url_for
import os, json, hashlib, time

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods = ["GET"])
def index():
    files = os.listdir(UPLOAD_FOLDER)

    html = "<h1>OFFLINE SYNC SERVER</h1>"
    html += "<h3>Uploaded Files: </h3>"

    for f in files:
        html += f"<li>{f}</li>"

    html += """
        <h3>Upload a file</h3>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    """
    return html

@app.route("/upload", methods = ["POST"])
def upload():
    if "file" not in request.files:
        return "No file sent", 400

    file = request.files["file"]
    
    if file.filename == "":
        return "No selected file"

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)