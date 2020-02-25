import requests
import urllib.parse
import json
from unfi_api.utils.http import response_to_json

"""
'https://ordermanagement.unfi.com/api/InteractiveReports/
"""
endpoint = r'https://ordermanagement.unfi.com/api/InteractiveReports/'


def get_products_by_top_sellers(token, account_number, user_id, **kwargs):
    """
    Available Parameters & Defaults
        'brandId': '',
        'region': 'West',
        'warehouse': '6',
        'sortOrder': 'QuantitySold',
        'sortDescription': 'DESC',
        'categoryId': '',
        'categoryName': '',
        'brandName': '',
        'productType': '',
        'upc': '',
        'productCode': '',
        'productDescription': '',
        'brandIds': '',
        'categoryIds': '',
        'allWords': '',
        'atLeastOneWord': '',
        'exactPhrase': '',
        'excludeWords': '',
        'searchProductInProductDescription': '',
        'searchProductInProductIngredients': '',
        'searchProductInAdditionalInfo': '',
        'searchProductInProductAttributes': '',
        'isAdminOrAccountManager': 'true',
        'pageSize': '50',
        'pageNumber': '1',
        'type': 'TopSellers',
        'isPrivateLabel': 'false',
        'departmentId': '',
        'startDate': 30 days before endDate,
        'endDate': 'today',
        'topRank': '50',
        'applyChannel': '0'
    :param user_id:
    :param account_number:
    :param token:
    :return: `dict`
    :rtype `dict`
    """
    endpoint_option = 'GetProductsByTopSellers_DssAsync'
    url = urllib.parse.urljoin(endpoint, endpoint_option)
    headers = {
        'authority': 'order_management.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 '
                      '(KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36',
        'origin': 'https://customers.unfi.com',
        'referer': 'https://customers.unfi.com/Pages/TopSellers.aspx?type=TopSellers',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = {
        'brandId': '',
        'region': 'West',
        'accountNumber': account_number,
        'userId': user_id,
        'warehouse': '6',
        'sortOrder': 'QuantitySold',
        'sortDescription': 'DESC',
        'categoryId': '',
        'categoryName': '',
        'brandName': '',
        'productType': '',
        'upc': '',
        'productCode': '',
        'productDescription': '',
        'brandIds': '',
        'categoryIds': '',
        'allWords': '',
        'atLeastOneWord': '',
        'exactPhrase': '',
        'excludeWords': '',
        'searchProductInProductDescription': '',
        'searchProductInProductIngredients': '',
        'searchProductInAdditionalInfo': '',
        'searchProductInProductAttributes': '',
        'isAdminOrAccountManager': 'true',
        'pageSize': '50',
        'pageNumber': '1',
        'type': 'TopSellers',
        'isPrivateLabel': 'false',
        'departmentId': '',
        'startDate': '01/23/2020',
        'endDate': '02/22/2020',
        'topRank': '50',
        'applyChannel': '0'
    }
    params.update(**kwargs)
    response = requests.get(url, headers=headers, params=params)
    return response_to_json(response)
