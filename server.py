from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

try:
    # Load our knowledge base from the CSV file
    locations_df = pd.read_csv("locations.csv")
    print("SUCCESS: locations.csv loaded into the bot's brain.")
except FileNotFoundError:
    print("ERROR: locations.csv not found. Make sure the file is in the same directory.")
    locations_df = pd.DataFrame() # Create an empty brain if file is missing

@app.route('/api/ask', methods=['POST'])
def ask_bot():
    user_message = request.json.get('message', '').lower()
    
    # Check for greetings first
    greetings = ['hello', 'hi', 'hey', 'gday', 'yo']
    if any(greet in user_message for greet in greetings):
        return jsonify({'reply': "Hello! How can I help you? You can ask me about service centre locations."})

    # Then, check for a location keyword from our data file
    for index, row in locations_df.iterrows():
        # Check if a city name from our file is in the user's message
        if str(row['city']).lower() in user_message:
            response_text = f"The {row['centre_name']} is located at {row['address']}, {row['city']} {row['postcode']}."
            return jsonify({'reply': response_text})

    # If nothing else matches, give a general "I don't know" response
    return jsonify({'reply': "Sorry, I don't have information on that. My main skill is finding service centres. Try asking 'where is the centre in Darwin?'"})

# This starts the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)