import requests
import csv
import time
from datetime import datetime
import schedule

# URL and station ID
URL = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"
STATION_ID = "66dbee85-0aca-11e7-82f6-3863bb44ef7c"
CSV_FILE = "/github/workspace/bike_availability.csv"

# Function to fetch and log data
def fetch_bike_data():
    try:
        response = requests.get(URL)
        data = response.json()
        
        # Find the station in the data
        station = next((s for s in data["data"]["stations"] if s["station_id"] == STATION_ID), None)
        
        if station:
            available_bikes = station["num_ebikes_available"]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Write data to CSV
            with open(CSV_FILE, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, available_bikes])
            
            print(f"{timestamp}: {available_bikes} bikes available")
        else:
            print(f"Station {STATION_ID} not found in data.")
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

# Function to schedule and run the task
def run_schedule():
    # Schedule task every 5 minutes between 8:00 AM and 10:00 AM
    schedule.every(5).minutes.do(fetch_bike_data).tag("bike_tracking")
    
    # Loop to keep the script running and checking for scheduled tasks
    while True:
        current_time = datetime.now().time()
        if current_time.hour >= 10:
            # Clear the schedule after 10 AM
            schedule.clear("bike_tracking")
            break
        schedule.run_pending()
        time.sleep(1)

# Main function to initialize CSV file and start schedule
def main():
    # Initialize CSV file with headers if it doesn't exist
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Available Bikes"])
    
    # Run the schedule between 8 AM and 10 AM
    print("Starting bike tracking schedule...")
    run_schedule()
    print("Finished bike tracking for the day.")

if __name__ == "__main__":
    main()
