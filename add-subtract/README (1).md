# Usage:

This program reads two numbers and an operation from a file and performs the requested operation on the two numbers and writes the result to a file.

## Request Data
1.) Main program creates a json object with the specified operation and 2 numbers \
2.) Main program sends the created json object to request.json in ./add-subtract \
3.) Microservice waits for the json object to be written to request.json \
4.) Once the data has finished writing, the microservice reads data from request.json 

Example Call: 

    request_data = {
        "operation": operation,
        "number1": number1,
        "number2": number2
    }

    request_path = os.path.join(service_dir, "request.json")
    with open(request_path, "w") as f:
        json.dump(request_data, f, indent=4)

## Receive Data
1.) Microservice creates a json object with the calculated result \
2.) Microservice sends the created json object to response.json \
3.) Main program waits for the json object to be written to response.json \
4.) Once the data has finished writing, the main program reads data from response.json in ./add-subtract

Example Call: 

    while True:
        try:
            with open(request_path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

        operation = data.get("operation")
        number1 = data.get("number1")
        number2 = data.get("number2")



## Diagram
<img width="1570" height="1176" alt="Screenshot (903)" src="https://github.com/user-attachments/assets/62f80177-c27f-421f-b1ec-86542bdebfa7" />


