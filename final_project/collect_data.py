import serial
import csv
import time

# Define serial port and baud rate
SERIAL_PORT = 'COM3'  # Update to match your system, e.g., '/dev/ttyUSB0' on Linux
BAUD_RATE = 9600
CSV_FILE = 'crop_data_log.csv'

# Health classification rules
def classify_health(temp, humidity, soil_moisture):
    if (20 <= temp <= 30 and 20 <= humidity <= 50 and 300 <= soil_moisture <= 600):
        return 'Healthy'
    elif ((15 <= temp <= 19 or 31 <= temp <= 35) and 
          (15 <= humidity <= 19 or 51 <= humidity <= 55) and 
          (200 <= soil_moisture <= 290 or 700 <= soil_moisture <= 790)):
        return 'Moderate'
    else:
        return 'Unhealthy'

def collect_data():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow serial connection to initialize

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(['Timestamp', 'Temperature', 'Humidity', 'SoilMoisture', 'Prediction'])

        try:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        temperature, humidity, soil_moisture = map(float, line.split(','))
                        soil_moisture = int(soil_moisture)

                        health_status = classify_health(temperature, humidity, soil_moisture)

                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([timestamp, temperature, humidity, soil_moisture, health_status])

                        print(f'{timestamp}, Temp: {temperature}, Humidity: {humidity}, Soil Moisture: {soil_moisture}, Health: {health_status}')
                        time.sleep(1)

                    except ValueError:
                        print("Invalid data received, skipping...")

        except KeyboardInterrupt:
            print("\nData collection stopped.")
            ser.close()

if __name__ == '__main__':
    collect_data()
