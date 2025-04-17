from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from ocr_processor import process_image, analyze_historical_period

app = Flask(__name__)

# Set the folder to save uploaded images
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    historical_analysis = None

    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part", 400

        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process the image with OCR
            extracted_text = process_image(file_path)

            # Analyze the historical period
            if extracted_text:
                historical_analysis = analyze_historical_period(extracted_text)

    return render_template('index.html', extracted_text=extracted_text, historical_analysis=historical_analysis)

if __name__ == '__main__':
    app.run(debug=True)
