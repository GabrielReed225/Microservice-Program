import json
import time
import os

# The microservice works inside its own directory
service_dir = "."
request_path = os.path.join(service_dir, "request.json")
response_path = os.path.join(service_dir, "response.json")

print("Add-Subtract microservice running...")

def open_file():
    while True:
        # Read request.json
        try:
            with open(request_path, "r") as f:
                data = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue
    return data

def validate_integers(number1, number2):
    if type(number1) != int or type(number2) != int:
        response_data = {
            "result": "Error: numbers must be integers.",
        }
        return response_data
    else:
        return "Proceed"

def closing(response_data):
    with open(response_path, "w") as f:
        json.dump(response_data, f, indent=4)
    os.remove(request_path)

def perform_operation(operation, number1, number2):
    if operation == "add":
        result = number1 + number2
    elif operation == "subtract":
        result = number1 - number2
    else:
        result = "Error: unsupported operation.",

    return {"result": result}

def add_subtract():
    data = open_file()
    operation = data.get("operation")
    number1 = data.get("number1")
    number2 = data.get("number2")

    response_data = validate_integers(number1, number2)
    if response_data == "Proceed":
        response_data = perform_operation(operation, number1, number2)

    closing(response_data)
    return

while True:
    add_subtract()