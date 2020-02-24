import requests
from unfi_api.utils.http import response_to_json


def get_products_by_full_text(token, query, account_number, user_id, region, warehouse, limit=1000,
                              organic_codes='', attribute_ids='', sales_filters='',
                              brand_ids='', category_ids='', page_number=1, **kwargs):
    """
    Full text search of products
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
    endpoint_url = 'https://ordermanagement.unfi.com/api/Brands/GetProductsByFullText'
    headers = {
        'authority': 'order_management.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
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

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response_to_json(response)


def get_brands(token, region, warehouse, account, page_size=9999, page_number=1, brand_prefix='A', **kwargs):
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

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response_to_json(response)


def get_products_by_brand_id(token, brand_id, account_number, user_id, page_size=1000, warehouse=6, region="West"):
    endpoint_url = 'https://ordermanagement.unfi.com/api/Brands/GetProductsByBrandId'
    headers = {
        'authority': 'order_management.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36',
        'dnt': '1',
        'origin': 'https://customers.unfi.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://customers.unfi.com/Pages/BrandDetail.aspx?brandId=27013&brandName=A%20CAJUN%20LIFE',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('brandId', brand_id),
        ('region', region),
        ('accountNumber', account_number),
        ('userId', user_id),
        ('warehouse', warehouse),
        ('sortOrder', 'BrandName'),
        ('sortDescription', 'ASC'),
        ('categoryId', ''),
        ('categoryName', ''),
        ('brandName', ''),
        ('productType', ''),
        ('upc', ''),
        ('productCode', ''),
        ('productDescription', ''),
        ('brandIds', ''),
        ('categoryIds', ''),
        ('allWords', ''),
        ('atLeastOneWord', ''),
        ('exactPhrase', ''),
        ('excludeWords', ''),
        ('searchProductInProductDescription', ''),
        ('searchProductInProductIngredients', ''),
        ('searchProductInAdditionalInfo', ''),
        ('searchProductInProductAttributes', ''),
        ('isAdminOrAccountManager', 'true'),
        ('pageSize', page_size),
        ('pageNumber', '1'),
        ('type', 'brand'),
        ('isPrivateLabel', 'false'),
    )

    response = requests.get(endpoint_url, headers=headers, params=params)
