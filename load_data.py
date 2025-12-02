import json
import sqlite3
from datetime import datetime

def load_data():
    """
    Loads device utilisation data from a JSON file into an SQLite database.
    """
    # 1. Connecting to the 'analytics.db' database that will hold all the json data, and if doesn't exist, then one will be created.
    conn = sqlite3.connect('analytics.db')
    cursor = conn.cursor()

    # 2. Creating 'device_utilisation' table with columns device_id, record_date, and utilisation_values, which will store the json data.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS device_utilisation (
            device_id TEXT NOT NULL,
            record_date TEXT NOT NULL,
            utilisation_values TEXT NOT NULL,
            PRIMARY KEY (device_id, record_date)
        );
    ''')
    
    # 3. Loading the json data from the file.
    with open('2_device_utilization_data.json', 'r') as f:
        data = json.load(f)

    # 4. Inserting each record into the database from the json file.
    for entry in data:
        device_id = entry['deviceID']
        original_date = entry['date']

        # multiple format date parsing
        record_date = None

        try:
            # Parsing the date from the original format (e.g., '1-Jan-2025')
            parsed_date = datetime.strptime(original_date, '%d-%b-%Y')

            # Reformating the date to follow YYYY-MM-DD
            record_date = parsed_date.strftime('%Y-%m-%d')

        except ValueError:
            print(f"Warning: Could not parse date '{original_date}' for device '{device_id}'. Skipping entry.")
            # Forcing the new format even if there's an error
            # try:
            #     parsed_date = datetime.strptime(original_date, '%Y-%m-%d')
            #     record_date = original_date

            # except ValueError:
            #     print(f"Warning: Could not parse date '{original_date}' for device '{device_id}'. Skipping entry.")
            #     continue  # Skip to the next entry if parsing fails
            
        # Converting the list of values back to a json string for storage.
        if record_date:
            utilisation_values = json.dumps(entry['values'])
            
            # Use 'INSERT OR REPLACE' to handle any duplicate entries if the script run again.
            cursor.execute('''
                INSERT OR REPLACE INTO device_utilisation (device_id, record_date, utilisation_values)
                VALUES (?, ?, ?);
            ''', (device_id, record_date, utilisation_values))

    # 5. Commiting the changes and closing the connection.
    conn.commit()
    conn.close()
    print("Data loaded successfully!")

if __name__ == '__main__':
    load_data()