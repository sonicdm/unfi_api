#!/usr/bin/env python3
import json
import requests


def response_to_json(response):
    """
    :type response: `requests.models.Response`
    :param response:
    :return:
    """
    error = None
    results = None
    status = None
    if not isinstance(response, requests.Response):
        error = f"response value must be type %r got %r instead" % (requests.Response, response)
    else:
        status = response.status_code
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
        "status": status,
        "results": results
    }
    return result
