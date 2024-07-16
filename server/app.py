from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.graph import process_user_input

app = Flask(__name__)
CORS(app)

def is_valid_input(text):
    # incase accident : input should be more than 8 characters long
    return len(text) > 8

@app.route('/api/data', methods=['POST'])
def process_data():
    data = request.json
    input_text = data.get('text', '')
    print("Received input:", input_text)  
    if not is_valid_input(input_text):
        return jsonify({"error": "Invalid input, must be more than 8 characters"}), 400
    
    try:
        # Process the user input and get the result
        processed_result = process_user_input(input_text)
        print("Processed result:", processed_result) 

        return jsonify(processed_result)
    except Exception as e:
        print(f"Error processing input: {e}")  
        return jsonify({"error": "An error occurred during processing"}), 500

@app.route('/api/processed', methods=['POST'])
def receive_processed_data():
    data = request.json
    print("Received processed data:", data) 
    generated = data.get('generated', '')
    grading_score = data.get('grading_score', 0)
    hellucination_score = data.get('hellucination_score', 0)
    # For simplicity, echoing the data back for the frontend to process
    return jsonify({
        "message": generated,
        "grading_score": grading_score,
        "hellucination_score": hellucination_score
    })

if __name__ == '__main__':
    app.run(debug=True)
