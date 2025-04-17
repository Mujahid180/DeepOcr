import easyocr
import google.generativeai as genai

# Initialize EasyOCR (you can change language codes to suit your needs)
reader = easyocr.Reader(['en'], gpu=False)

# Configure Google Gemini AI
genai.configure(api_key="AIzaSyBCuS6N-Rfgleo3WurTfdG35BCb7yRK1O8")  # Replace with your API key

model = genai.GenerativeModel("gemini-1.5-pro-latest")  # or another model if you prefer

def process_image(image_path):
    try:
        # Perform OCR on the image
        result = reader.readtext(image_path)
        text = "\n".join([item[1] for item in result])  # Extract the detected text
        return text
    except Exception as e:
        return str(e)

def analyze_historical_period(text):
    try:
        # Use Google Gemini AI to analyze the historical period of the text
        response = model.generate_content(f"Analyze the historical period of this text:\n{text}")
        return response.text if response.text else "Analysis failed."
    except Exception as e:
        return f"Error analyzing historical period: {str(e)}"
