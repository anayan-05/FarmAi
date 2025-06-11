from flask import Flask, render_template, jsonify
import serial
import joblib

app = Flask(__name__)

model = joblib.load('model/crop_health_model.pkl')

SERIAL_PORT = 'COM3'  # Adjust based on your system
BAUD_RATE = 9600

def get_live_sensor_data():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
            line = ser.readline().decode('utf-8').strip()
            if line:
                try:
                    temperature, humidity, soil_moisture = map(float, line.split(','))
                    return temperature, humidity, soil_moisture
                except ValueError:
                    return None
            else:
                return None
    except serial.SerialException:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    data = get_live_sensor_data()
    if data:
        temperature, humidity, soil_moisture = data
        prediction = model.predict([[temperature, humidity, soil_moisture]])[0]
        result = {
            'temperature': temperature,
            'humidity': humidity,
            'soil_moisture': soil_moisture,
            'prediction': prediction
        }
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to read data from Arduino'}), 500

if __name__ == '__main__':
    app.run(debug=False)
