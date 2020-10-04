import requests
# for timestamp info
from time import strftime, localtime
from datetime import datetime

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

    # This api is showing forecast for five days so i couldnt use first one
    url_forecast = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'

    forecast_response = requests.get(url_forecast).json()

    # gettiing dict with temperature, date and icon for forecast
    def day_forecast():
        """"
        This function is taking API respone and looping trough all elements finding data for night temp, specified its acually 12:00 PM,
         and taking from this data: temperature and date

         Returning two list:
         First contains dicts and each dict contians info about temperautre and timestamp and weather icon
         Second contains week days
        """
        temp_day = []
        for i in forecast_response['list']:
            foo = '12:00:00'
            if foo in i['dt_txt']:
                dictor = {
                    'date': i['dt'],
                    'temp': i['main']['temp'],
                    'icon': i['weather'][0]['icon'],
                    'date_txt': i['dt_txt']
                }
                temp_day.append(dictor)

        # This for loop is selecting all DT from respoonse and making list of it
        temport = []
        for d in temp_day:
            temport.append(d['date'])

        # This loop converting timestamp DT format to week days names and making list of it
        dates_formated = []
        for value in temport:
            dates_formated.append(
                datetime.utcfromtimestamp(value).strftime('%A'))
        return [temp_day, dates_formated]

    def night_forecast():
        """"
        This function is taking API respone and looping trough all elements finding data for night temp, specified its acually 3:00 AM,
         and taking from this data: temperature and date

         Returning list that contains dicts and each dict contians info about temperautre and timestamp
        """

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

    return render_template('index.html', weather=weather, temp=temp_int, time=time,
                           day_forecast=day_forecast, night_forecast=night_forecast)


@app.route('/<string:city>/<string:date>')
def city_forecast(city, date):

    API_KEY = '0cecf8365f48c0900489013ff0623926'

    # it explain itself(taking user input and making it capital letter)
    city = city.capitalize()

    # gettiing dict with temperature, date and icon for forecast every 3 hours
    url_forecast = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'

    forecast_response = requests.get(url_forecast).json()

    def detail_forecast():
        lst_details = []
        for item in forecast_response['list']:
            if date in item['dt_txt']:
                if '12:00' in item['dt_txt']:
                    weather_detail = {
                        'city': city,
                        'date': item['dt_txt'],
                        'temperature': item['main']['temp_max'],
                        'feels_like': item['main']['feels_like'],
                        'humidity': item['main']['humidity'],
                        'wind': item['wind']['speed'],
                        'description': item['weather'][0]['description'],
                        'icon': item['weather'][0]['icon'],
                        'pressure': item['main']['pressure']
                    }
                    lst_details.append(weather_detail)
        return lst_details

    detail_forecast = detail_forecast()

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

    return render_template('city_forecast.html', date=date, detail_forecast=detail_forecast, time=time,
                           forecast_hours=forecast_hours, forecast_temperatures=forecast_temperatures)


if __name__ == '__main__':
    app.run(debug=True)
