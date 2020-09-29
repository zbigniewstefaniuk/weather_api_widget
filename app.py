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

    night_forecast = night_forecast()

    return render_template('index.html', weather=weather, temp=temp_int, time=time, day_forecast=day_forecast, night_forecast=night_forecast)


@app.route('/<string:city>/<string:date>')
def city_forecast(city, date):
    API_KEY = '0cecf8365f48c0900489013ff0623926'

    # it explain itself
    city = city.capitalize()
    # getting api
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'

    response = requests.get(url).json()

    weather = {
        'city': city,
        'temperature': response['main']['temp'],
        'humidity': response['main']['humidity'],
        'wind': response['wind']['speed'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    # gettiing dict with temperature, date and icon for forecast every 3 hours
    url_forecast = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'

    forecast_response = requests.get(url_forecast).json()

    def hour_day_forecast():
        temp_hour = []
        for i in forecast_response['list']:
            foo = date
            if foo in i['dt_txt']:
                dictor = {
                    'date': i['dt_txt'],
                    'temp': i['main']['temp'],
                    'icon': i['weather'][0]['icon'],
                }
                temp_hour.append(dictor)
        return temp_hour

    hour_day_forecast = hour_day_forecast()

    def forecast_hours():
        hour_lst = []
        for hour in hour_day_forecast:
            hour_lst.append(hour['date'][11:16])
        return hour_lst

    forecast_hours = forecast_hours()

    def forecast_temperatures():
        temps_lst = []
        for temper in hour_day_forecast:
            rounded_temp = round(temper['temp'], 1)
            temps_lst.append(str(rounded_temp) + ' °C')
        return temps_lst

    forecast_temperatures = forecast_temperatures()

    time = strftime('%A %H:%M', localtime())


    return render_template('city_forecast.html',date=date, weather=weather, time=time, forecast_hours=forecast_hours, forecast_temperatures=forecast_temperatures)


if __name__ == '__main__':
    app.run(debug=True)
