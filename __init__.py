from flask import Flask, render_template, request, redirect
from threading import Thread
# from werkzeug.security import secure_filename

app = Flask(__name__)
app.config.from_object("config")

from helper import *

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def upload_file():

	# A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file:
        # file.filename = secure_filename(file.filename)
        output = upload_to_s3(file, app.config["S3_BUCKET"])
        thread = Thread(target=start_transcribe, args=(file.filename,))
        thread.start()
        return str(output)

    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)