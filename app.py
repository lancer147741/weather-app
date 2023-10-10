import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        api_key = os.getenv('api_key')
        base_url = "http://api.openweathermap.org/data/2.5/forecast?appid={}&units=metric&cnt=7&q=".format(api_key)
        complete_url = base_url + city
        response = requests.get(complete_url)
        data = response.json()

        if data['cod'] != '404':
            current_temperature = data['list'][0]['main']['temp']
            weather_description = data['list'][0]['weather'][0]['description']

            # Получаем прогноз погоды на 7 дней
            forecast = []
            for day in data['list']:
                forecast.append({
                    'date': day['dt_txt'].split()[0],
                    'temperature': day['main']['temp'],
                    'description': day['weather'][0]['description']
                })

            if request.is_json:
                return jsonify({
                    'current_temperature': current_temperature,
                    'weather_description': weather_description,
                    'forecast': forecast,
                    'city': city
                })

            return render_template('index.html', current_temperature=current_temperature,
                                   weather_description=weather_description, forecast=forecast, city=city)
        else:
            return render_template('error.html')

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
