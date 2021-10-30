from .products import get_product_by_int_id, get_product_data, get_product_attributes_by_product_by_int_id
import urllib.parse
from unfi_api.utils.http import response_to_api_response, response_to_api_response
from unfi_api.products import Product, Pricing, Attribute, Ingredients, Marketing, NutritionFacts
from unfi_api.api.base_classes import APICore, Endpoint
import requests
import random

products_api_endpoint = r'https://products.unfi.com/api/Products/'


class Products(Endpoint):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.api: APICore = api
        self.api_endpoint: str = products_api_endpoint
        pass

    def get_product_by_int_id(self, product_int_id: int):
        url = urllib.parse.urljoin('https://products.unfi.com/api/Products/', str(product_int_id))
        response = self.api.session.get(url)
        return response_to_api_response(response)

    def get_product_attributes_by_product_by_int_id(self, product_int_id):
        endpoint = "attributes"
        product_url = urllib.parse.urljoin('https://products.unfi.com/api/Products/', str(product_int_id) + "/")
        url = urllib.parse.urljoin(product_url, endpoint)
        response = self.api.session.get(url)
        return response_to_api_response(response)

    def get_product_ingredients_by_product_by_int_id(self, product_int_id):
        endpoint = "ingredients"
        product_url = urllib.parse.urljoin('https://products.unfi.com/api/Products/', str(product_int_id) + "/")
        url = urllib.parse.urljoin(product_url, endpoint)
        response = self.api.session.get(url)
        # response = requests.get(url, cookies=self.api.session.cookies)
        return response_to_api_response(response)

    def get_product_marketing_by_product_by_int_id(self, product_int_id):
        endpoint = "marketing"
        product_url = urllib.parse.urljoin('https://products.unfi.com/api/Products/', str(product_int_id) + "/")
        url = urllib.parse.urljoin(product_url, endpoint)
        response = self.api.session.get(url)
        # response = requests.get(url, cookies=self.api.session.cookies)
        return response_to_api_response(response)

    def get_product_nutrition_by_product_by_int_id(self, product_int_id):
        endpoint = "nutrition"
        product_url = urllib.parse.urljoin('https://products.unfi.com/api/Products/', str(product_int_id) + "/")
        url = urllib.parse.urljoin(product_url, endpoint)
        response = self.api.session.get(url)
        # response = requests.get(url, cookies=self.api.session.cookies)
        return response_to_api_response(response)

    def get_west_product_data(self, product_code):
        product_data_url = "https://products.unfi.com/api/Products/GetWestProductData"
        params = {
            "customerNumber": self.api.account.strip(),
            "productCode": product_code
        }
        header = {
            "authorization": self.api.auth_token
        }
        # self.api.session.headers['origin'] = products_api_endpoint
        response = self.api.session.get(product_data_url, params=params, headers=header)
        # response = requests.get(product_data_url, headers=header, params=params)
        return response_to_api_response(response)

    def get_product_image(self, product_int_id):
        url = f"https://products.unfi.com/api/Images/{product_int_id}"
        response = self.api.session.get(url)
        error = None
        data = None
        status = None
        if not isinstance(response, requests.Response):
            error = f"response value must be type %r got %r instead" % (requests.Response, response)
        else:
            status = response.status_code
            if not response.status_code == 200:
                data = None
                error = response.reason
            else:
                data = response.content

        result = {
            "error": error,
            "status": status,
            "data": data,
            "content": response.content,
            "response": response
        }
        return result

    def product(self, product_code, product_int_id):
        product = None
        product_info = None
        product_detail = None
        product_data = None
        ingredients = None
        attributes = None
        marketing = None
        nutrition_facts = None
        pricing = None

        if not all((product_int_id, product_code)):
            raise AttributeError("Must provide product_int_id or product_code")

        if product_int_id and product_code:
            product_info_result = self.get_product_by_int_id(product_int_id)
            if not product_info_result['error']:
                product_info = product_info_result['data']
            product_data_result = self.get_west_product_data(product_code)
            if not product_data_result['error']:
                product_data = product_data_result['data']
            product_detail_result = self.api.order_management.product_detail.get_product_detail_by_int_id(
                product_int_id)
            if not product_detail_result['error']:
                product_detail = product_detail_result['data'][0]

        if product_info and product_data:
            product_data_combined = product_info.copy()
            product_data_combined.update(product_data)
            attribute_result = self.get_product_attributes_by_product_by_int_id(product_int_id)
            ingredients_result = self.get_product_ingredients_by_product_by_int_id(product_int_id)
            marketing_result = self.get_product_marketing_by_product_by_int_id(product_int_id)
            nutrition_result = self.get_product_nutrition_by_product_by_int_id(product_int_id)
            pricing_result = self.api.brands.get_product_pricing_detail(product_code)

            if not nutrition_result['error']:
                nutrition_facts = nutrition_result['data']
            if not marketing_result['error']:
                marketing = marketing_result['data']
            if not attribute_result['error']:
                attributes = attribute_result['data']
            if not ingredients_result['error']:
                ingredients = ingredients_result['data']
            if not pricing_result['error']:
                pricing = pricing_result['data']

            product = Product(
                product_data=product_data, product=product_info, marketing=marketing, ingredients=ingredients,
                nutrition_facts=nutrition_facts, attributes=attributes, pricing=pricing
            )
        else:
            raise Exception("Product data failed to fetch with error: " + product_info_result['error'])

        return {
            "product": product,
            "detail": product_detail,
            "data": product_data,
            "ingredients": ingredients,
            "attributes": attributes,
            "marketing": marketing,
            "nutrition": nutrition_facts,
            "pricing": pricing
        }
