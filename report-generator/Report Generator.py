import json
import sqlite3
import time
import os
import csv

service_dir = "."
request_path = os.path.join(service_dir, "request.json")
response_path = os.path.join(service_dir, "response.json")


print("Generate Report microservice running...")

while True:
    # Read request.json
    try:
        with open(request_path, "r") as request_file:
            data = json.load(request_file)
    except (json.JSONDecodeError, FileNotFoundError):
        time.sleep(0.1)
        continue

    # Get file type/ path
    data_source = data.get("data_source")
    file_path = data.get("file_path", None)
    internal_data = data.get("data", None)
    output_csv = data.get("output_csv", "report.csv")
    output_csv = os.path.join(service_dir, output_csv)

    # Check for improper input
    failure = 0

    if data_source == "db":
        if file_path is None:
            failure = 1
        else:
            connection = sqlite3.connect(file_path)
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM Expenses")

            columns = [description[0] for description in cursor.description]

            rows = cursor.fetchall()
            connection.close()

            with open(output_csv, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(columns)
                writer.writerows(rows)
    elif data_source == "dictionary":
        if internal_data is None:
            failure = 1
        else:
            dictionary_data = data.get("data", {})
            headers = ["key", "value"]

            with open(output_csv, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                for key, value in dictionary_data.items():
                    writer.writerow([key, value])
    else:
        failure = 1

    if failure == 1:
        response = {
            "status": "failure",
            "message": "Improper data source provided",
            "csv_file": None
        }
    elif failure == 0:
        response = {
            "status": "success",
            "message": "CSV file generated",
            "csv_file": output_csv
        }

    with open("response.json", "w") as response_file:
        json.dump(response, response_file, indent=4)
    os.remove(request_path)
