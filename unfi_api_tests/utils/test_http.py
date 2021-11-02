from unittest import TestCase

import requests
from unfi_api.api.response import APIResponse
from unfi_api.utils.http import response_to_api_response, response_to_json


class TestResponseToAPIResponse(TestCase):
    def test_response_to_api_response(self):
        test_url = 'https://my-json-server.typicode.com/typicode/demo/posts'
        response = requests.get(test_url)
        api_response = response_to_api_response(response)
        self.assertIsInstance(api_response, APIResponse)
        self.assertEqual(api_response.status, response.status_code)
        self.assertEqual(api_response.data, response.json())
        self.assertEqual(api_response.content_type, response.headers.get('content-type'))
        self.assertEqual(api_response.text, response.text)


class TestResponseToJson(TestCase):
    def test_response_to_json(self):
        test_url = 'https://my-json-server.typicode.com/typicode/demo/posts'
        response = requests.get(test_url)
        json = response_to_json(response)
        self.assertIsInstance(json, dict)
        self.assertEqual(json['data'], response.json())
        self.assertEqual(json['status'], response.status_code)
        self.assertEqual(json['content_type'], response.headers.get('content-type'))
        self.assertEqual(json['text'], response.text)
        
