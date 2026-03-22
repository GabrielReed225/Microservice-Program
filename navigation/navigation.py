import json
import time
import os

# The microservice works inside its own directory
service_dir = "."
request_path = os.path.join(service_dir, "request.json")
response_path = os.path.join(service_dir, "response.json")

print("navigation microservice running...")

while True:
    try:
        with open(request_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        time.sleep(0.1)
        continue

    print(f"Received: {data}")

    key = data.get("key")
    file = data.get("file")
    file = os.path.normpath(file)
    location = data.get("location")


    if key is None:
        response_data = {
            "result": "Error: No key provided.",
        }
        with open(response_path, "w") as f:
            json.dump(response_data, f, indent=4)
        os.remove(request_path)
        continue

    # Validate file existence
    # Covers non-nested and nested
    try:
        with open(file, "r") as f:
            file_data = json.load(f)
        if location is None:
            location = file_data
        elif type(location) != str and type(location) != list:
            response_data = {
                "result": "Error: Invalid request path.",
            }
            with open(response_path, "w") as f:
                json.dump(response_data, f, indent=4)
            os.remove(request_path)
            continue
        elif type(location) == str:
            location = file_data.get(location, file_data)
        else:
            node = file_data
            for part in location:
                if part not in node or not isinstance(node[part], dict):
                    node[part] = {}
                node = node[part]

            location = node

        if key in location:
            response_data = {
                "result": location[key],
            }
            with open(response_path, "w") as f:
                json.dump(response_data, f, indent=4)
            os.remove(request_path)
            continue
        else:
            response_data = {
                "result": "Error: Key not found.",
                }
            with open(response_path, "w") as f:
                json.dump(response_data, f, indent=4)
            os.remove(request_path)
            continue

    except FileNotFoundError:
        response_data = {
            "result": "Error: File Not Found.",
        }
        with open(response_path, "w") as f:
            json.dump(response_data, f, indent=4)
        os.remove(request_path)
        continue
