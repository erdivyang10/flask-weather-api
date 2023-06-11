from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather_report(city)

    return render_template('weather.html', weather_data=weather_data)   


def get_weather_report(city):
    api_key = "5d80ad505ac74b74b94248617a4ec1fa"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Change to "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["cod"] == 200:
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            weather_report = f"Weather in {city}: {description}, Temperature: {temperature}°C, Humidity: {humidity}%"
            return weather_report
        else:
            return "Error: Failed to retrieve weather data."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


if __name__ == '__main__':
    app.run()