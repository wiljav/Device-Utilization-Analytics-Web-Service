import json
import sqlite3
from flask import Flask, request, jsonify

# Initiating Flask web app
app = Flask(__name__)

# Function to create a connection to 'analytics.db' database
def get_db_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect('analytics.db')
    conn.row_factory = sqlite3.Row  # Allows to access columns by name
    return conn

# Top 5 most utilized devices (on average) on a specific date:
@app.route('/top-5') # Mapping the API url '/top-5' to function get_top_5_devices()
def get_top_5_devices():
    """
    To get top 5 devices average readings, all the data is retrieved from the database.
    Each row of this data is iterated then the average is calculated using (sum of values for each device) / (length of values for each device).
    The average is: Sum of values / Number of values. Example is for device 71875627 -> 23418.974398 / 288 = 81.32:
    devices values: [92.065254, 85.166246, 70.286736, 90.692088, 90.839473, etc]
    devices avg: 81.3158833264
    """
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Missing 'date' parameter"}), 400

    # Start connection with the DB
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT device_id, utilisation_values FROM device_utilisation WHERE record_date = ?;"
    cursor.execute(query, (date,))
    
    devices = []
    for row in cursor.fetchall():
        utilisation_values = json.loads(row['utilisation_values'])
        average_utilisation = sum(utilisation_values) / len(utilisation_values)
        
        devices.append({
            "device_id": row['device_id'],
            "average_utilisation": round(average_utilisation, 2)
        })
    
    conn.close()
    
    # Sort the list and return the top 5
    top_5_devices = sorted(devices, key=lambda x: x['average_utilisation'], reverse=True)[:5]
    return jsonify(top_5_devices)

# Hourly rolling average of device utilization of a device between dates
@app.route('/hourly-average') # Mapping the API url '/hourly-average' to function get_hourly_average()
def get_hourly_average():
    """
    For 24h per day and 60min per 1 hour, the data is of 5min interval for each record. Therefore, for each day the data was sliced into (60 min / 5 min = 12) chunks.
    The average is: Sum of hours / Number of hours. Example for device 44243EC9 -> 930.84 / 12 = 77.57:
        hours values: [72.999972, 66.602152, 75.938904, 92.116699, 94.150858, 62.90512, 78.637163, 75.784627, 85.717229, 79.25555, 55.135626, 91.594429]
        hours avg: 77.56986075
    """
    device_id = request.args.get('device_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not all([device_id, start_date, end_date]):
        return jsonify({"error": "Missing one or more parameters: device_id, start_date, end_date"}), 400

    # Start connection with the DB
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT record_date, utilisation_values FROM device_utilisation WHERE device_id = ? AND record_date BETWEEN ? AND ? ORDER BY record_date;"
    cursor.execute(query, (device_id, start_date, end_date))
    
    hourly_averages = []
    
    for row in cursor.fetchall():
        utilisation_values = json.loads(row['utilisation_values'])
        
        # Calculate hourly averages from the 5-minute interval data
        for i in range(24): # 24h per day
            hour_values = utilisation_values[i*12:(i+1)*12] # Slicing the data into an array of 12 chunks (hours). At i = 0 -> i*12:(0+1)*12 = 0:12, therefore, the first hour has utilisation_values[0:12] and next hour is utilisation_values[12:24]
            hourly_avg = sum(hour_values) / len(hour_values) # Sum of hours / number of hours
            
            hourly_averages.append({
                "date": row['record_date'],
                "hour": f"{i:02d}:00", # To ensure the hours have decimal integer i.e. d, leading 02 to ensure a width of 2 decimals.
                "average_utilisation": round(hourly_avg, 2) # To ensure the hourly_avg has 2 decimal points for accuracy
            })
    # Close connection with the DB
    conn.close()
    
    return jsonify(hourly_averages)


if __name__ == '__main__':
    # Running the API in the 'main' function
    app.run(debug=True)