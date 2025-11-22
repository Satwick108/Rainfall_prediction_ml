from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np
import requests

app = Flask(__name__)

# Load the trained model
with open("rainfall_prediction_model.pkl", "rb") as file:
    model = pickle.load(file)

WEATHER_API_KEY = "8859e69ef4b66b2b8e77b85237477d1e"


feature_names = ['pressure', 'dewpoint', 'humidity', 'cloud', 'sunshine', 'winddirection', 'windspeed']


@app.route('/')
def home():
    return render_template('index.html')  


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        input_features = [float(data[f]) for f in feature_names]
        input_array = np.array(input_features).reshape(1, -1)

        prediction = model.predict(input_array)[0]
        result = "Rainfall" if prediction == 1 else "No Rainfall"

        return render_template('result.html', prediction=result)  

    except Exception as e:
        return render_template('result.html', prediction=f"Error: {str(e)}")  


@app.route('/get_weather', methods=['GET'])
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and Longitude required"}), 400  

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        weather_info = {
            "pressure": weather_data["main"]["pressure"],
            "dewpoint": weather_data["main"].get("dew_point", 10),  
            "humidity": weather_data["main"]["humidity"],
            "cloud": weather_data["clouds"]["all"],
            "sunshine": 100 - weather_data["clouds"]["all"],  
            "winddirection": weather_data["wind"]["deg"],
            "windspeed": weather_data["wind"]["speed"]
        }

        return jsonify(weather_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error


@app.route('/predict_again')
def predict_again():
    return render_template('index.html')  


if __name__ == '__main__':
    app.run(debug=True)
