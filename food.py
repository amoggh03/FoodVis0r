from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import base64
from PIL import Image
import pytesseract
import openai

app = Flask(__name__)



# Directory to save images
SAVE_DIR = "/Users/amoggha03/Desktop/College/HACKS/FoodHealthBot/IMAGES"
os.makedirs(SAVE_DIR, exist_ok=True)

# Predefined medical and allergy information
predefined_allergies = "nil"
predefined_medical_conditions = "nil"
personalDetails = ""

# Variables to store extracted text
extractedText1 = ""
extractedText2 = ""
important_text_extracted_from_camera = ""

# Initial messages for the chatbot
messages = [
    {
        "role": "system",
        "content": (
            f"You are a medical assistant who works as a doctor with knowledge about allergies, dietary restrictions, and serious health conditions. "
            f"Users will provide their personal details- Age, weight, and height, as well as any allergies or medical conditions they have. "
            f"Your response should start with 'No' or 'Yes' if it's a question, followed by a brief explanation and a moderation suggestion. "
            f"Personal details: {personalDetails}. Predefined allergies: {predefined_allergies}. Predefined medical conditions: {predefined_medical_conditions}."
        )
    },
    {
        "role": "assistant",
        "content": "Hey, how can I help you today?"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saveImage', methods=['POST'])
def save_image():
    data = request.json
    global extractedText1, extractedText2, personalDetails, important_text_extracted_from_camera

    try:
        # Update personal details and extract reports
        personalDetails = data.get('personalDetails', '')
        allergy_report = data.get('allergyReport', '')
        medical_report = data.get('medicalReport', '')
        uploaded_image_data = data.get('imageSrc')



        if allergy_report:
            extractedText1 = process_image(allergy_report, 'allergy_report.jpg')
            print("\nExtracted Allergy Report Text:", extractedText1)

        if medical_report:
            extractedText2 = process_image(medical_report, 'medical_report.jpg')
            print("\nExtracted Medical Report Text:", extractedText2)
        if uploaded_image_data:
            important_text_extracted_from_camera = process_image(uploaded_image_data, 'uploaded_image.jpg')
        print("\nExtracted Text from Camera Image:", important_text_extracted_from_camera)
        return jsonify({'success': True, 'extracted_text1': extractedText1, 'extracted_text2': extractedText2, 'extracted_text': important_text_extracted_from_camera}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

def process_image(image_data, filename):
    image_data = base64.b64decode(image_data.split(',')[1])
    image_path = os.path.join(SAVE_DIR, filename)
    with open(image_path, 'wb') as f:
        f.write(image_data)
    return extract_text_from_image(image_path)

@app.route('/ingredients', methods=['POST'])
def ingredients():
    try:
        ingredients = request.json.get('ingredients')
        print("Ingredients:", ingredients)

        # Save and extract ingredients
        directory = os.path.join(SAVE_DIR, 'ingredients.txt')
        with open(directory, 'w') as f:
            f.write(ingredients)

        extracted_text = extract_text_from_text_file(directory)
        print("\nExtracted Text:", extracted_text)

        medical_info = extract_medical_info(extracted_text)
        combined_text = (
            f"Predefined allergies: {predefined_allergies}. "
            f"Predefined medical conditions: {predefined_medical_conditions}. "
            f"Personal details: {personalDetails}. "
            f"Allergy report: {extracted_text}. "
            f"Medical Info: {medical_info}"
            f"Important extracted text: {important_text_extracted_from_camera}."

        )
        print("\nCombined Text:", combined_text)

        ingredient_analysis = analyze_ingredients(combined_text)
        return jsonify({'success': True, 'extracted_text': extracted_text, 'ingredient_analysis': ingredient_analysis}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

def extract_text_from_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

@app.route('/chat', methods=['POST'])
def chat():
    global messages
    try:
        user_message = request.json.get('message')
        combined_text = (
            f"Predefined allergies: {predefined_allergies}. "
            f"Predefined medical conditions: {predefined_medical_conditions}. "
            f"Personal details: {personalDetails}. "
            f"Allergy report text: {extractedText1}. "
            f"Medical report text: {extractedText2}. "
            f"User query: {user_message}"
            f"Important extracted text: {important_text_extracted_from_camera}."

        )
        print("\nUser Message:", user_message)
        print("\nCombined Text Sent to GPT:", combined_text)

        messages.append({"role": "user", "content": user_message})

        chat_completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a medical assistant with knowledge about allergies and health conditions."},
                {"role": "user", "content": combined_text}
            ]
        )

        assistant_reply = chat_completion.choices[0].message['content']
        messages.append({"role": "assistant", "content": assistant_reply})
        print("\nAssistant Reply:", assistant_reply)

        return jsonify({'success': True, 'reply': assistant_reply}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def extract_medical_info(combined_text):
    # Placeholder for extracting medical information from combined_text
    return "Simulated medical info from combined text."

@app.route('/saveCombinedText', methods=['POST'])
def save_combined_text():
    global personalDetails, extractedText1, extractedText2

    try:
        data = request.json
        personal_details = data.get('personalDetails', {})
        weight = personal_details.get('weight', '')
        age = personal_details.get('age', '')
        height = personal_details.get('height', '')

        personalDetails = f"Weight: {weight} kg, Age: {age} years, Height: {height} cm"
        extractedText1 = data.get('allergyInput', '')
        extractedText2 = data.get('medicalInfoInput', '')

        print("\nUpdated Personal Details:", personalDetails)
        print("Updated Allergy Report:", extractedText1)
        print("Updated Medical Info:", extractedText2)

        return jsonify({'success': True}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/input', methods=['POST'])
def get_input():
    return redirect(url_for('askme'))

@app.route('/askme')
def askme():
    return render_template('askme.html')

@app.route('/updatePersonalDetails', methods=['POST'])
def update_personal_details():
    global personalDetails
    try:
        data = request.json
        personalDetails = data.get('personalDetails', '')
        print("\nUpdated Personal Details:", personalDetails)
        return jsonify({'success': True}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)