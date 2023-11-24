from flask import Flask, request, render_template_string, jsonify
import requests

app = Flask(__name__)

# URL of the external API (configurable)
API_URL = "http://apiserver:7001"

@app.route('/form_submit', methods=['POST'])
def form_submit():
    # Extract form data and convert to JSON
    form_data = request.form
    json_data = form_data.to_dict()

    # Send JSON data to the external API
    response = requests.post(API_URL, json=json_data)

    # Parse the JSON response from the API
    response_data = response.json()

    # Display the API's response
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>API Response</title>
        </head>
        <body>
            <p>API Response:</p>
            <h1>{{ message }}</h1>
            <p>
                <button onclick="window.history.back();">Return to the form</button>
            </p>
        </body>
        </html>
    """, message=response_data.get("message"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
