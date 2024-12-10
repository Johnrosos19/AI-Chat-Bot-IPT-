from flask import Flask, request, render_template, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS  # To enable CORS if needed

app = Flask(__name__)

# Enable CORS
CORS(app)

# Set up your API key and configuration
api_key = "AIzaSyBmZgvtRbSumwif4yNWbxGCTBl4T_YHlq8"  # Replace with your API key
genai.configure(api_key=api_key)

# Create the model with configuration
generation_config = {
    "temperature": 0.3,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are IPT Chatbot, a highly knowledgeable and friendly assistant specializing in integrated programming and technology. Your role is to provide accurate, detailed, and beginner-friendly answers about programming concepts, frameworks, and tools, as well as advanced technical topics like APIs, cloud computing, DevOps, AI/ML, and software architecture.\n\nYou are IPT Chatbot, an assistant focused exclusively on Integrated Programming and Technology. Respond only to questions directly related to Integrated Programming and Technology.\n\nIf a user asks a question that does not pertain to Integrated Programming and Technology, reply with:\n'Sorry, I'm here to assist only with Integrated Programming and Technology topics. Please ask a relevant question.'\n\n-Simplify complex concepts when necessary but provide sufficient technical depth for clarity.\n-Offer examples in code snippets, diagrams, or step-by-step instructions where applicable.\n-Always specify programming languages or technologies used in your examples.\n-Encourage best practices and provide helpful links to documentation or resources if asked.\n-Respond concisely and professionally, and adapt to the user's level of expertise (beginner, intermediate, advanced).\n\n-Debugging assistance and solutions for common coding problems.\n-Recommendations on tools, libraries, and frameworks.\n-Explanations of technical concepts in integrated programming and emerging technologies.\n-Suggestions for project structures or workflows in various development environments.\"\n",
)

# Start a chat session
chat_session = model.start_chat(
    history=[]
)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the request
    user_message = request.json.get('message')
    
    if not user_message:
        return jsonify({"error": "Message not provided"}), 400

    # Send message to the chatbot
    response = chat_session.send_message(user_message)
    
    # Return the response from the chatbot
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)
