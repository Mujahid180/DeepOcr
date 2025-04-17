from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from ocr_processor import process_image, analyze_historical_period

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = ""
    historical_analysis = ""

    if request.method == "POST":
        if "image" in request.files:
            image = request.files["image"]
            if image.filename != "":
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image.save(image_path)

                extracted_text = process_image(image_path)
                historical_analysis = analyze_historical_period(extracted_text)

    return render_template("index.html", extracted_text=extracted_text,
                           historical_analysis=historical_analysis)

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
