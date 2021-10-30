import requests
import urllib.parse
from unfi_api.utils.http import response_to_json, response_to_api_response
from bs4 import BeautifulSoup
from unfi_api import settings
brands_base_url = 'https://ordermanagement.unfi.com/api/Brands/'


def get_products_by_full_text(session, token, query, account_number, user_id, region, warehouse, limit=1000,
                              organic_codes='', attribute_ids='', sales_filters='',
                              brand_ids='', category_ids='', page_number=1, **kwargs):
    """
    Full text search of products
    :param session:
    :param token:
    :param query:
    :param account_number:
    :param user_id:
    :param region:
    :param warehouse:
    :param limit:
    :param organic_codes:
    :param attribute_ids:
    :param sales_filters:
    :param brand_ids:
    :param category_ids:
    :param page_number:
    :param kwargs:
    :return:
    """
    endpoint = 'GetProductsByFullText'
    endpoint_url = urllib.parse.urljoin(brands_base_url, endpoint)
    headers = {
        'authority': 'order_management.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'origin': 'https://customers.unfi.com',
        'referer': 'https://customers.unfi.com/Pages/ProductSearch.aspx?SearchTerm=search',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = {
        'fullTextQuery': query,
        'organicCodes': organic_codes,
        'attributeIds': attribute_ids,
        'salesFilters': sales_filters,
        'brandIds': brand_ids,
        'categoryIds': category_ids,
        'region': region,
        'warehouse': warehouse,
        'accountNumber': account_number,
        'userId': user_id,
        'isAdminOrAccountManager': 'true',
        'pageSize': 1000,
        'pageNumber': page_number
    }
    if kwargs:
        params.update(**kwargs)
    echo_url = urllib.parse.urljoin("http://localhost:8000", endpoint)
    # echo = requests.get(echo_url, headers=headers, params=params).json()
    response = session.get(endpoint_url, headers=headers, params=params)
    return response_to_json(response)


def get_brands(session, token, region, warehouse, account, page_size=9999, page_number=1, brand_prefix='A', **kwargs):
    endpoint_url = 'https://ordermanagement.unfi.com/api/Brands/GetBrands'
    headers = {
        'origin': 'https://customers.unfi.com',
        'authorization': token
    }

    params = (
        ('brandPrefix', brand_prefix),
        ('pageSize', page_size),
        ('pageNumber', page_number),
        ('region', region),
        ('whsNumber', warehouse),
        ('CustomerNumber', account),
    )
    params = {
        'brandPrefix': brand_prefix,
        'pageSize': page_size,
        'pageNumber': page_number,
        'region': region,
        'whsNumber': warehouse,
        'CustomerNumber': account
    }
    if kwargs:
        params.update(**kwargs)

    response = session.get(endpoint_url, headers=headers, params=params)
    return response_to_json(response)


def get_products_by_brand_id(session, token, account_number, user_id, warehouse, region, brand_id, sort_order='ASC',
                             sort_description="BrandName", category_id='', category_name='', brand_name='',
                             product_type='', upc='', product_code='', product_description='', brand_ids='',
                             category_ids='', all_words='', at_least_one_word='', exact_phrase='', exclude_words='',
                             search_product_in_product_description='', search_product_in_product_ingredients='',
                             search_product_in_product_attribbutes='', search_product_in_additional_info='',
                             page_size=1000, page_number=1, _type='brand', is_private_label='false'):
    endpoint = 'GetProductsByBrandId'
    endpoint_url = urllib.parse.urljoin(brands_base_url, endpoint)
    headers = {
        'authority': 'order_management.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36',
        'origin': 'https://customers.unfi.com',
        'referer': 'https://customers.unfi.com/Pages/BrandDetail.aspx?brandId=27013&brandName=A%20CAJUN%20LIFE',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = {
        'brandId': brand_id,
        'region': region,
        'accountNumber': account_number,
        'userId': user_id,
        'warehouse': warehouse,
        'sortOrder': sort_description,
        'sortDescription': sort_order,
        'categoryId': category_id,
        'categoryName': category_name,
        'brandName': brand_name,
        'productType': product_type,
        'upc': upc,
        'productCode': product_code,
        'productDescription': product_description,
        'brandIds': brand_ids,
        'categoryIds': category_ids,
        'allWords': all_words,
        'atLeastOneWord': at_least_one_word,
        'exactPhrase': exact_phrase,
        'excludeWords': exclude_words,
        'searchProductInProductDescription': search_product_in_product_description,
        'searchProductInProductIngredients': search_product_in_product_ingredients,
        'searchProductInAdditionalInfo': search_product_in_additional_info,
        'searchProductInProductAttributes': search_product_in_product_attribbutes,
        'isAdminOrAccountManager': 'true',
        'pageSize': page_size,
        'pageNumber': page_number,
        'type': _type,
        'isPrivateLabel': is_private_label
    }
    echo_url = urllib.parse.urljoin("http://localhost:8000", endpoint)
    # echo = requests.get(echo_url, headers=headers, params=params).json()
    response = session.get(endpoint_url, headers=headers, params=params)
    return response_to_json(response)


def get_product_details_from_service(session, token, product_code, account_number):
    """
    gets pricing table from the api and converts to json
    :param session:
    :param token:
    :param product_code:
    :param account_number:
    :return:
    """
    endpoint = 'GetProductDetailsFromService'
    endpoint_url = urllib.parse.urljoin(brands_base_url, endpoint)
    headers = {
        'authority': 'order_management.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36',
        'origin': 'https://customers.unfi.com',
        'referer': 'https://customers.unfi.com/Pages/BrandDetail.aspx?brandId=27013&brandName=A%20CAJUN%20LIFE',
        'accept-language': 'en-US,en;q=0.9',
    }
    params = (
        ('custNum', account_number),
        ('prodCode', product_code),
    )

    response = session.get(endpoint_url, headers=headers, params=params)
    # error = None
    # status = None
    # results = []
    # if not isinstance(response, requests.Response):
    #     error = f"response value must be type %r got %r instead" % (requests.Response, response)
    # else:
    #     status = response.status_code
    #     if not response.status_code == 200:
    #         results = None
    #         error = response.reason
    #     else:
    #         results = parse_pricing_table(response.content)
    #
    # result = {
    #     "error": error,
    #     "status": status,
    #     "data": results
    # }
    return response_to_api_response(response)


def parse_pricing_table(page):
    results = []

    pricing_soup = BeautifulSoup(page, features=settings.beautiful_soup_parser)

    table_soup = pricing_soup.find_all('table')[1]
    headers = {}
    for idx, tr in enumerate(table_soup.find_all('tr')):
        if idx == 0:
            for i, x in enumerate(tr.find_all("th")):
                headers[i] = str(x.text).lower().replace(".", "").replace(" ", "_")
        else:
            row = [x.text.replace(r"\r", "").replace(r"\n", "").replace(" ", "") for x in tr.find_all('td')]
            prices = {}
            for i, x in enumerate(row):
                prices[headers[i]] = x
            results.append(prices)
    return results
