import json


def response_to_json(response):
    error = None
    results = None
    if not response.status_code == 200:
        results = None
        error = response.reason
    else:
        try:
            results = response.json()

        except json.JSONDecodeError as exception:
            error = "Invalid Json Response"

    result = {
        "error": error,
        "status": response.status_code,
        "results": results
    }
    return result
