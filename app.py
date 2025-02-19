from flask import Flask, request, jsonify
import openai
import base64

app = Flask(__name__)

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"

# Function to analyze clothing image
def analyze_clothing(base64_image):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a fashion expert. Analyze the clothing in the image and suggest matching outfits."},
            {"role": "user", "content": [
                {"type": "text", "text": "Analyze this clothing item and suggest a matching outfit."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
