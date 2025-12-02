# Device Utilization Analytics Web Service

This is a simple and offline web app developed in Python to analyze device utilisation data.

## Project Structure
- `2_device_utilization_data.json`: The source data file.
- `load_data.py`: A script to load the JSON data into a local SQLite database `analytics.db` - Can be accessed with DBeaver, if needed.
- `app.py`: The Flask web app that provides the analytics endpoints.
- `requirements.txt`: Lists the Python dependencies.
- `README.md`: This documentation.

## Installation and Running

### Prerequisites

- Python 3.13
- `pip` (Python package installer)

**Optional**:
- DBeaver (to access `analytics.db`)

### Setup
#### Create and Activate a Virtual Environment
navigate the the project's directory, then execute the commands below:
1. Create a virtual environment
```sh
python -m venv .env
```

2. Activate the virtual environment:
- On Windows
```sh
.env\Scripts\activate
```

- On macOS/Linux
```sh
source .env/bin/activate
```

#### Install Dependencies
```sh
pip install -r requirements.txt
```
Libraries used that do not need to be installed are: `json`, `sqlite3`, `datetime`

### Database Population
1. Run the data loading script to create the `analytics.db` file and populate it with data.
```sh
python load_data.py
```

2. Run the web app:
```sh
flask run
```


## Usage
The web app has two entry points, these are:

1. [Top 5 most utilized devices (on average) on a date](http://127.0.0.1:5000/top-5?date=2025-01-01)
```sh
http://127.0.0.1:5000/top-5?date=2025-01-01
```

2. [Hourly rolling average of device utilization of a device between dates](http://127.0.0.1:5000/hourly-average?device_id=44243EC9&start_date=2025-01-02&end_date=2025-01-07)
```sh
http://127.0.0.1:5000/hourly-average?device_id=44243EC9&start_date=2025-01-02&end_date=2025-01-07
```