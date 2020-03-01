"""

product catalog api calls

"""

import requests
import urllib.parse
from unfi_api.utils.http import response_to_json

products_api_endpoint = r'https://products.unfi.com/api/Products/'


def get_product_attributes(token, product_id):
    header = {
        'authorization': '{token}'.format(token=token, )
    }


def get_product_data(token, customer_number, product_code):
    header = {
        'authorization': '{token}'.format(token=token, )
    }

    product_data_url = "https://products.unfi.com/api/Products/GetWestProductData" \
                       "?customerNumber={custnum}" \
                       "&productCode={product_code}"
    params = {
        "customerNumber": customer_number,
        "productCode": product_code
    }

    data_response = requests.get(product_data_url, headers=header)
    data_result = data_response.json()


def get_product_by_int_id(token, product_int_id):
    headers = {
        "authorization": token
    }
    url = urllib.parse.urljoin('https://products.unfi.com/api/Products/', str(product_int_id))
    response = requests.get(url)
    return response_to_json(response)
