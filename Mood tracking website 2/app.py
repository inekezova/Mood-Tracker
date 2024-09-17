from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)

API_KEY = '6fa86f1d253937f318dbaaefa8de5ecb'  # Use your OpenWeather API key
CITY = 'eindhoven'
CSV_FILE = 'feeling_data.csv'

# Function to fetch weather data
def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_info = {
            "city": data['name'],
            "temperature": data['main']['temp'],
            "description": data['weather'][0]['description'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
            "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_info
    else:
        return None

# Function to save the feeling and weather data to CSV
def save_to_csv(feeling_data, file_name=CSV_FILE):
    df = pd.DataFrame([feeling_data])

    try:
        df.to_csv(file_name, mode='a', header=not pd.read_csv(file_name).empty, index=False)
    except FileNotFoundError:
        df.to_csv(file_name, mode='w', header=True, index=False)

# Flask route to handle user input and display the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['name']
        mood = request.form['mood']

        # Fetch weather data
        weather_data = get_weather(API_KEY, CITY)

        if weather_data:
            # Prepare data for saving
            record = {
                "user_name": user_name,
                "morning_feeling": mood,
                **weather_data
            }

            # Save data to CSV
            save_to_csv(record)

            # Redirect to the same page after saving
            return redirect('/')
        else:
            return render_template('index.html', error="Could not fetch weather data.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
