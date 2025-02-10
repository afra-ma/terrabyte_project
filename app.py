from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': '208.109.49.193',
    'user': 'techvs',
    'password': 'Techvs@250',
    'database': 'techvs'
}

def fetch_data():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Fetch the latest data from the terabyte table
        query = "SELECT soil, temperature, humidity, smoke FROM terabyte ORDER BY id DESC LIMIT 6"
        cursor.execute(query)
        data = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()

        return data
    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return []

@app.route('/')
def dashboard():
    # Fetch data from the database
    data = fetch_data()

    # Extract data for charts
    labels = [f"{i}:00" for i in range(6)]  # Example labels (00:00 to 05:00)
    soil_data = [row['soil'] for row in data]
    temperature_data = [row['temperature'] for row in data]
    humidity_data = [row['humidity'] for row in data]
    smoke_data = [row['smoke'] for row in data]

    return render_template('dashboard.html', labels=labels, soil_data=soil_data,
                           temperature_data=temperature_data, humidity_data=humidity_data,
                           smoke_data=smoke_data)

@app.route('/disease-detection')
def disease_detection():
    return render_template('disease_detection.html')

@app.route('/irrigation-control')
def irrigation_control():
    return render_template('irrigation_control.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)