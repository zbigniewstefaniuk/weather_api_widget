import requests
# for timestamp info
from time import strftime, localtime

# Flask imports
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    API_KEY = '0cecf8365f48c0900489013ff0623926'
    
    # when user first time hits site, showing him Kraków Weather
    try:
        user_input = request.form.get('user_city')
        city = user_input.capitalize()
    except:
        city = 'Krakow'
    # getting api
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'

    response = requests.get(url).json()

    # If name of city is wrong spell or unknown
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting {city.title()} ERROR = {message}'

    weather = {
        'city': city,
        'temperature': response['main']['temp'],
        'humidity': response['main']['humidity'],
        'wind': response['wind']['speed'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    time = strftime('%A %H:%M', localtime())
    temp_float = weather.get('temperature')
    temp_int = round(temp_float)

    # Forecast for next 5 days/nights

    url_forecast = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'

    forecast_response = requests.get(url_forecast).json()

    # gettiing dict with temperature, date and icon for forecast
    def day_forecast():
        temp_day = []
        for i in forecast_response['list']:
            foo = '12:00:00'
            if foo in i['dt_txt']:
                dictor = {
                    'date': i['dt_txt'],
                    'temp': i['main']['temp'],
                    'icon': i['weather'][0]['icon'],
                }
                temp_day.append(dictor)
        return temp_day

    def night_forecast():
        temp_night = []
        for i in forecast_response['list']:
            foo = '03:00:00'
            if foo in i['dt_txt']:
                dictor = {
                    'date': i['dt_txt'],
                    'temp': i['main']['temp'],
                }
                temp_night.append(dictor)
        return temp_night

    day_forecast = day_forecast()
    print(day_forecast)
    print(night_forecast())
    night_forecast = night_forecast()

    return render_template('index.html', weather=weather, temp=temp_int, time=time, day_forecast=day_forecast, night_forecast=night_forecast)


if __name__ == '__main__':
    app.run(debug=True)
