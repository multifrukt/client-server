from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# URL of the external API (configurable)
API_URL = "http://ubuntu:7001"

@app.route('/form_submit', methods=['POST'])
def form_submit():
    # Extract form data
    form_data = request.form

    # Send data to the external API
    response = requests.post(API_URL, data=form_data)

    # Display the API's response
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>API Response</title>
        </head>
        <body>
            <h1>API Response</h1>
            <p>{{ response }}</p>
        </body>
        </html>
    """, response=response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
