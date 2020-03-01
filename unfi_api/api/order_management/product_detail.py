from urllib import parse
import requests

from unfi_api.utils.http import response_to_json

product_detail_endpoint = 'https://ordermanagement.unfi.com/api/ProductDetail/'


def get_product_detail_by_int_id(token, product_int_id, region, account_number, warehouse, user_id):

    header = {
        'authorization': token
    }
    endpoint_name = "GetProductDetailByProductIntId"
    url = parse.urljoin(product_detail_endpoint, endpoint_name)
    params = {
        'productIntId': product_int_id,
        'region': region,
        'accountNumber': account_number,
        'warehouse': warehouse,
        'userId': user_id
    }

    result = requests.get(url, headers=header, params=params)
    return response_to_json(result)

