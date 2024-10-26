import json
import time
import logging
import os
import schedule
import tkinter as tk

# Configure logging
logging.basicConfig(filename='script2.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Path to JSON file
json_file = 'result.json'

# Function to update the flag in the JSON file to False
def set_flag_false():
    if os.path.exists(json_file):
        with open(json_file, 'r+') as file:
            try:
                content = json.load(file)
                content['flag'] = False  # Set the flag to False
                file.seek(0)
                json.dump(content, file, indent=4)
                file.truncate()

                logging.info("Updated flag to False.")
            except json.JSONDecodeError:
                logging.error("Error decoding JSON.")
    else:
        logging.error(f"{json_file} not found.")

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
    root.title("Script 2: JSON Monitor")

    timestamp_label = tk.Label(root, text="Timestamp: N/A", font=('Arial', 16))
    timestamp_label.pack(pady=10)

    flag_label = tk.Label(root, text="Flag: N/A", font=('Arial', 16))
    flag_label.pack(pady=10)

    update_gui()
    root.mainloop()

# Schedule the function to run every 3 minutes
schedule.every(3).minutes.do(set_flag_false)

# Start Tkinter GUI in a separate thread
import threading
threading.Thread(target=display_gui).start()

# Run scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
