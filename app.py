from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import requests

app = Flask(__name__)

# Load the trained model
with open("rainfall_prediction_model.pkl", "rb") as file:
    model = pickle.load(file)

# OpenWeatherMap API Key (Replace with your actual API key)
WEATHER_API_KEY = "8859e69ef4b66b2b8e77b85237477d1e"

# Feature names expected by the model
feature_names = ['pressure', 'dewpoint', 'humidity', 'cloud', 'sunshine', 'winddirection', 'windspeed']


@app.route('/')
def home():
    return render_template('index.html')  # Home Page with Form


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        input_features = [float(data[f]) for f in feature_names]
        input_array = np.array(input_features).reshape(1, -1)

        prediction = model.predict(input_array)[0]
        result = "Rainfall" if prediction == 1 else "No Rainfall"

        return render_template('result.html', prediction=result)  # Navigate to result page

    except Exception as e:
        return render_template('result.html', prediction=f"Error: {str(e)}")  # Error Handling


@app.route('/get_weather', methods=['GET'])
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400  # Bad Request

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        # Extract necessary fields
        weather_info = {
            "pressure": weather_data["main"]["pressure"],
            "dewpoint": weather_data["main"].get("dew_point", 10),  # Some APIs may not provide dew point
            "humidity": weather_data["main"]["humidity"],
            "cloud": weather_data["clouds"]["all"],
            "sunshine": 100 - weather_data["clouds"]["all"],  # Approximate sunshine as inverse of cloud %
            "winddirection": weather_data["wind"]["deg"],
            "windspeed": weather_data["wind"]["speed"]
        }

        return jsonify(weather_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error


@app.route('/predict_again')
def predict_again():
    return render_template('index.html')  # Redirect to Home Page


if __name__ == '__main__':
    app.run(debug=True)
