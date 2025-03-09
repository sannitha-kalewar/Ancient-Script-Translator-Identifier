import os
import pytesseract
from flask import Flask, request, jsonify
from PIL import Image
from googletrans import Translator
import openai

app = Flask(__name__)
translator = Translator()
openai.api_key = "your-openai-api-key"  # Set your OpenAI API key

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)
    
    text = extract_text(image_path)
    translated_text = translate_text(text)
    
    return jsonify({'original_text': text, 'translated_text': translated_text})

def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()

def translate_text(text, target_language='en'):
    translated = translator.translate(text, dest=target_language)
    return translated.text

@app.route('/analyze_sculpture', methods=['POST'])
def analyze_sculpture():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)
    
    with open(image_path, 'rb') as img_file:
        response = openai.Image.create(
            model="gpt-4-vision-preview",
            image=img_file,
            tasks=["describe"]
        )
    
    description = response['description']
    translated_description = translate_text(description)
    
    return jsonify({'description': description, 'translated_description': translated_description})

if __name__ == '__main__':
    app.run(debug=True)
