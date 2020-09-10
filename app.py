import requests

# Flask imports
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    city = 'Zakopane'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=0cecf8365f48c0900489013ff0623926'

    response = requests.get(url).json()

    weather = {
        'city': city,
        'temperature': response['main']['temp'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    return render_template('index.html', weather=weather)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    city = request.form.get('user_city')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=0cecf8365f48c0900489013ff0623926'

    response = requests.get(url).json()

    weather = {
        'city': city,
        'temperature': response['main']['temp'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    return render_template('weather.html', weather=weather)


if __name__ == '__main__':
    app.run(debug=True)
