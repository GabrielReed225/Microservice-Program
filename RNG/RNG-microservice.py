import json
import time
import os
import random

# The microservice works inside its own directory
service_dir = "."
request_path = os.path.join(service_dir, "request.json")
response_path = os.path.join(service_dir, "response.json")

print("RNG microservice running...")

while True:
    try:
        with open(request_path, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        time.sleep(0.1)
        continue

    # Set action variable
    action = data.get("action")

    # Check if valid action provided
    if action not in ["generate_integer", "generate_choice"]:
        response_data = {
            "status": "error",
            "result": "Error: invalid action.",
        }
        with open(response_path, "w") as f:
            json.dump(response_data, f, indent=4)
        os.remove(request_path)
        continue

    # Select random value from list for generate_choice action
    if action == "generate_choice":
        values = data.get("values")
        if not isinstance(values, list) or len(values) == 0:
            response_data = {
                "status": "error",
                "result": "Error: no values provided.",
            }
            with open(response_path, "w") as f:
                json.dump(response_data, f, indent=4)
            os.remove(request_path)
            continue
        result = random.choice(values)

    # Select random integer
    else:
        min_val = data.get("minimum")
        max_val = data.get("maximum")
        if min_val is None:                 # Default to 1 if empty
            min_val = 1
        if max_val is None:                 # Default to 1000 if empty
            max_val = 1000

        # Check if provided min/max is integer
        if not isinstance(min_val, int) or not isinstance(max_val, int):
            response_data = {
                "status": "error",
                "result": "Error: numbers must be integers.",
            }
            with open(response_path, "w") as f:
                json.dump(response_data, f, indent=4)
            os.remove(request_path)
            continue

        # Check if min/max are valid range
        if max_val < min_val:
            response_data = {
                "status": "error",
                "result": "Error: minimum number greater than maximum number.",
            }
            with open(response_path, "w") as f:
                json.dump(response_data, f, indent=4)
            os.remove(request_path)
            continue

        result = random.randint(min_val, max_val)

    # Send result response
    response_data = {
        "status": "success",
        "result": result,
    }
    with open(response_path, "w") as f:
        json.dump(response_data, f, indent=4)
    os.remove(request_path)
