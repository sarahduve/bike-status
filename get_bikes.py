import requests
import csv
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# URL and station ID
URL = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"
STATION_ID = "66dbee85-0aca-11e7-82f6-3863bb44ef7c"
CSV_FILE = "bike_availability.csv"

# Function to fetch and log data
def fetch_bike_data():
    try:
        response = requests.get(URL)
        data = response.json()

        # Find the station in the data
        station = next((s for s in data["data"]["stations"] if s["station_id"] == STATION_ID), None)

        if station:
            available_bikes = station["num_ebikes_available"]
            timestamp = datetime.now().astimezone(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S")

            # Append data to CSV, adding headers if the file is new
            file_exists = os.path.isfile(CSV_FILE)
            with open(CSV_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Timestamp", "Available Bikes"])
                writer.writerow([timestamp, available_bikes])

            print(f"{timestamp}: {available_bikes} bikes available")
        else:
            print(f"Station {STATION_ID} not found in data.")

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_bike_data()
