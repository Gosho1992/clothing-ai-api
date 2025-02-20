from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Ensure OpenAI API key is stored securely (Use Environment Variable in Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Get JSON request
        data = request.json
        image_data = data.get("image")  # Expecting base64 encoded image

        if not image_data:
            return jsonify({"error": "No image provided"}), 400

        # OpenAI API Call (New API Format)
        client = openai.OpenAI(api_key=openai.api_key)

        response = client.chat.completions.create(
            model="gpt-4o",  # Use GPT-4o Mini for cost efficiency
            messages=[
                {"role": "system", "content": "You are a fashion expert that suggests matching outfits."},
                {"role": "user", "content": "Analyze this clothing item and suggest a matching outfit."},
                {"role": "assistant", "content": f"Here is the image for analysis: {image_data}"}
            ],
            max_tokens=300
        )

        return jsonify({"analysis": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)



   
