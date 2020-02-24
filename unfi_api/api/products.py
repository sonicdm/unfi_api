"""

product catalog api calls

"""

import requests


def get_categories():
    headers = {
        'dnt': '1',
        'sec-fetch-site': 'same-site',
    }

    params = (
        ('region', 'West'),
        ('whsNumber', '6'),
        ('CustomerNumber', '001014    \n-H'),
    )

    response = requests.get('https://ordermanagement.unfi.com/api/Categories/GetCategoriesOrderByDepartments',
                            headers=headers, params=params)


def get_categories_by_brand_id(token, brand_id, cust_num):
    headers = {
        'authority': 'ordermanagement.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 '
                      '(KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36',
        'origin': 'https://customers.unfi.com',
        'referer': 'https://customers.unfi.com/Pages/BrandDetail.aspx?brandId=27013&brandName=A%20CAJUN%20LIFE',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('brandId', brand_id),
        ('brandName', ''),
        ('region', 'West'),
        ('whsNumber', '6'),
        ('CustomerNumber', cust_num),
    )

    response = requests.get('https://ordermanagement.unfi.com/api/Brands/GetCategoriesByBrandID', headers=headers,
                            params=params)


def get_brands(token):
    endpoint_url = 'https://ordermanagement.unfi.com/api/Brands/GetBrands'
    headers = {
        'origin': 'https://customers.unfi.com',
    }

    params = (
        ('brandPrefix', 'A'),
        ('pageSize', '9999'),
        ('pageNumber', '1'),
        ('region', 'West'),
        ('whsNumber', '6'),
        ('CustomerNumber', '001014    '),
    )

    response = requests.get(endpoint_url, headers=headers, params=params)


def get_products_by_brand_id(token, brand_id, account_number, user_id, page_size=1000, warehouse=6, region="West"):
    endpoint_url = 'https://ordermanagement.unfi.com/api/Brands/GetProductsByBrandId'
    headers = {
        'authority': 'ordermanagement.unfi.com',
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


def get_products_by_top_sellers(token):
    endpoint_url = 'https://ordermanagement.unfi.com/api/InteractiveReports/GetProductsByTopSellers_DssAsync'
    headers = {
        'authority': 'ordermanagement.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 '
                      '(KHTML, like Gecko) '
                      'Chrome/80.0.3987.116 Safari/537.36',
        'dnt': '1',
        'origin': 'https://customers.unfi.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://customers.unfi.com/Pages/TopSellers.aspx?type=TopSellers',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('brandId', ''),
        ('region', 'West'),
        ('accountNumber', '001014    '),
        ('userId', '140963'),
        ('warehouse', '6'),
        ('sortOrder', 'QuantitySold'),
        ('sortDescription', 'DESC'),
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
        ('pageSize', '50'),
        ('pageNumber', '1'),
        ('type', 'TopSellers'),
        ('isPrivateLabel', 'false'),
        ('departmentId', ''),
        ('startDate', '01/23/2020'),
        ('endDate', '02/22/2020'),
        ('topRank', '50'),
        ('applyChannel', '0'),  # find top sellers by similar accounts 0 or True
    )

    response = requests.get(endpoint_url, headers=headers, params=params)


def get_products_by_full_text(token, query, account_number, user_id, limit=10000):
    endpoint_url = 'https://ordermanagement.unfi.com/api/Brands/GetProductsByFullText'
    headers = {
        'authority': 'ordermanagement.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'authorization': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'dnt': '1',
        'origin': 'https://customers.unfi.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://customers.unfi.com/Pages/ProductSearch.aspx?SearchTerm=search',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('fullTextQuery', query),
        ('organicCodes', ''),
        ('attributeIds', ''),
        ('salesFilters', ''),
        ('brandIds', ''),
        ('categoryIds', ''),
        ('region', 'West'),
        ('warehouse', '6'),
        ('accountNumber', account_number),
        ('userId', user_id),
        ('isAdminOrAccountManager', 'true'),
        ('pageSize', limit),
        ('pageNumber', '1'),
    )

    response = requests.get(endpoint_url, headers=headers, params=params)
