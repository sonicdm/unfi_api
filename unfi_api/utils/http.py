#!/usr/bin/env python3
import json
from requests import Response, status_codes
from unfi_api.api.response import APIResponse


def response_to_json(response: Response) -> dict:
    """
    :type response: `requests.models.Response`
    :param response:
    :return:
    """
    error = None
    data = None
    status = None
    if not isinstance(response, Response):
        error = f"response value must be type %r got %r instead" % (Response, response)
    else:
        status = response.status_code
        if not response.ok:
            data = None
            error = response.reason
        else:
            try:
                data = response.json()

            except json.JSONDecodeError as exception:
                error = ""

    result = {
        "error": error,
        "status": status,
        "data": data,
        "content": response.content,
        "text": response.text,
        "response": response
    }
    return result


def response_to_api_response(response) -> APIResponse:
    """
    :type response: `requests.models.Response`
    :param response:
    :return:
    """
    result = response_to_json(response)
    return APIResponse.parse_obj(result)
