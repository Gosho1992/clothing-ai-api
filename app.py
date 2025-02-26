import openai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ensure this is set in Render Environment Variables

def analyze_clothing(base64_image):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a fashion expert that suggests matching outfits."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this clothing item and suggest a matching outfit."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_data = data.get("image")  # Expecting base64-encoded image

    if not image_data:
        return jsonify({"error": "No image provided"}), 400

    # Call OpenAI API
    result = analyze_clothing(image_data)

    return jsonify({"analysis": result})

# ✅ Fix: Use Render's PORT dynamically
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render assigns dynamic ports
    app.run(debug=True, host='0.0.0.0', port=port)
