from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_NINJAS_KEY")  # Set this key in your Render dashboard

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': '🎯 Horoscope API is running!',
        'usage': '/horoscope/today/<sunsign>',
        'example': '/horoscope/today/leo'
    })

@app.route('/horoscope/today/<sunsign>', methods=['GET'])
def get_horoscope(sunsign):
    url = "https://api.api-ninjas.com/v1/horoscope"
    headers = {
        'X-Api-Key': API_KEY
    }
    params = {
        'zodiac': sunsign.lower()
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return jsonify({
            'date': data.get('date'),
            'sunsign': data.get('zodiac'),
            'horoscope': data.get('horoscope')
        })
    else:
        return jsonify({
            'error': f"API error {response.status_code}",
            'details': response.text
        }), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
