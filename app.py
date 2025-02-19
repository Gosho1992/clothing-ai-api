import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "No image provided"}), 400

    # Call OpenAI API
    result = analyze_clothing(image_data)
    
    return jsonify({"analysis": result})

def analyze_clothing(image):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a fashion expert that suggests matching outfits."},
            {"role": "user", "content": "Analyze this clothing item and suggest a matching outfit."},
            {"role": "assistant", "content": image}
        ],
        max_tokens=300
    )
    
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

   
