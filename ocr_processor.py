import easyocr
import cv2
import numpy as np
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key="AIzaSyBCuS6N-Rfgleo3WurTfdG35BCb7yRK1O8")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Initialize EasyOCR
reader = easyocr.Reader(["hi", "en"], gpu=False)

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 31, 2)
    kernel = np.ones((1, 1), np.uint8)
    processed_image = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return processed_image

def process_image(image_path):
    try:
        detected_text = reader.readtext(image_path, detail=0)
        return "\n".join(detected_text) if detected_text else "No text detected."
    except Exception as e:
        return f"OCR Failed: {str(e)}"

def analyze_historical_period(text):
    try:
        response = model.generate_content(f"Analyze the historical period of this text:\n{text}")
        return response.text if response.text else "Analysis failed."
    except Exception as e:
        return f"Error analyzing historical period: {str(e)}"
