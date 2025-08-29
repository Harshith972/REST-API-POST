# app.py

# Import necessary classes from the Flask framework
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

@app.route('/bfhl', methods=['POST'])
def process_data():
    """
    Handles POST requests to the /bfhl endpoint.
    Processes an array of data and returns a structured JSON response.
    """
    try:
        # Get the JSON data from the request body
        payload = request.get_json()

        # Check if the payload is valid and contains the 'data' key
        if not payload or 'data' not in payload or not isinstance(payload['data'], list):
            # Return a 400 Bad Request error if the input is invalid
            return jsonify({
                "is_success": False,
                "error": "Invalid input: JSON payload must contain a 'data' key with an array."
            }), 400

        data = payload['data']

        # --- User and College Information ---
        # These values are hardcoded as per the example.
        user_id = "john_doe_17091999"
        email = "john@xyz.com"
        roll_number = "ABCD123"

        # --- Data Processing ---
        # Initialize lists and variables to store the processed data
        odd_numbers = []
        even_numbers = []
        alphabets = []
        special_characters = []
        total_sum = 0
        alphabet_string = ""

        # Iterate over each item in the input 'data' array
        for item in data:
            item_str = str(item)
            # Check if the item is a number (integer or float)
            if item_str.replace('.', '', 1).isdigit() or (item_str.startswith('-') and item_str[1:].replace('.', '', 1).isdigit()):
                try:
                    number = int(item_str)
                    total_sum += number
                    if number % 2 == 0:
                        even_numbers.append(item_str)
                    else:
                        odd_numbers.append(item_str)
                except ValueError:
                    # Handle cases like "12.34" which are numbers but not integers for the even/odd logic
                    special_characters.append(item_str)
            # Check if the item is a string of alphabets
            elif item_str.isalpha():
                alphabets.append(item_str.upper())
                alphabet_string += item_str
            # Otherwise, it's a special character
            else:
                special_characters.append(item_str)

        # --- Concatenated and Alternating Caps String Logic ---
        # 1. Reverse the concatenated string of alphabets
        reversed_string = alphabet_string[::-1]
        concat_string = ""
        # 2. Apply alternating capitalization
        for i, char in enumerate(reversed_string):
            if i % 2 == 0:
                concat_string += char.upper()
            else:
                concat_string += char.lower()

        # --- Construct the Final Response ---
        # Create the response dictionary with all the processed data
        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": str(total_sum),
            "concat_string": concat_string
        }

        # Return the successful response with a 200 OK status code
        return jsonify(response), 200

    except Exception as e:
        # --- Error Handling ---
        # If any unexpected error occurs, log it and send a 500 Internal Server Error response
        app.logger.error(f"An error occurred: {e}")
        return jsonify({
            "is_success": False,
            "error": "An internal server error occurred."
        }), 500

# This block allows the script to be run directly for development
if __name__ == '__main__':
    # Runs the Flask app. debug=True enables auto-reloading on code changes.
    app.run(debug=True, port=5000)


