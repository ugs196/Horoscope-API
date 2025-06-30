from flask import Flask, jsonify
import requests
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_NINJAS_KEY")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': '🔮 Horoscope API is running!',
        'usage': '/horoscope/today/<sunsign>',
        'example': '/horoscope/today/leo',
        'supported_signs': [
            "aries", "taurus", "gemini", "cancer", "leo", "virgo",
            "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
        ]
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

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'date': data.get('date'),
                'sunsign': sunsign.lower(),
                'horoscope': data.get('horoscope')
            })
        else:
            return jsonify({
                'error': f"API error {response.status_code}",
                'details': response.text
            }), response.status_code
    except Exception as e:
        return jsonify({
            'error': 'Exception occurred while fetching horoscope',
            'details': str(e)
        }), 500

if __name__ == "__main__":
    app.run()
