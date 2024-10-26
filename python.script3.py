import json
import time
import logging
from datetime import datetime
import os
import schedule
import tkinter as tk

# Configure logging
logging.basicConfig(filename='script1.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Path to JSON file
json_file = 'result.json'

# Function to create or update the JSON file
def update_json_file():
    data = {
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "flag": False
    }

    # If file exists, update the timestamp and flag
    if os.path.exists(json_file):
        with open(json_file, 'r+') as file:
            try:
                content = json.load(file)
                content['timestamp'] = data['timestamp']
                content['flag'] = False  # Reset the flag to False
            except json.JSONDecodeError:
                logging.error("Error decoding JSON, recreating file.")
                content = data  # Reinitialize if there's an error

            file.seek(0)
            json.dump(content, file, indent=4)
            file.truncate()

        logging.info("Updated JSON with timestamp and flag=False.")
    else:
        # Create the file with initial values
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=4)
        logging.info("Created new JSON file with timestamp and flag=False.")

# Tkinter GUI to monitor JSON data
def display_gui():
    def update_gui():
        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                content = json.load(file)
                timestamp_label.config(text=f"Timestamp: {content['timestamp']}")
                flag_label.config(text=f"Flag: {content['flag']}")
        root.after(3000, update_gui)  # Refresh every 3 seconds

    root = tk.Tk()
    root.title("Script 1: JSON Monitor")

    timestamp_label = tk.Label(root, text="Timestamp: N/A", font=('Arial', 16))
    timestamp_label.pack(pady=10)

    flag_label = tk.Label(root, text="Flag: N/A", font=('Arial', 16))
    flag_label.pack(pady=10)

    update_gui()
    root.mainloop()

# Schedule the update function to run every 10 minutes
schedule.every(10).minutes.do(update_json_file)

# Start Tkinter GUI in a separate thread
import threading
threading.Thread(target=display_gui).start()

# Run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)

