import requests
from unfi_api.utils.http import response_to_json


def get_categories(session):
    headers = {
        'dnt': '1',
        'sec-fetch-site': 'same-site',
    }

    params = (
        ('region', 'West'),
        ('whsNumber', '6'),
        ('CustomerNumber', '001014    \n-H'),
    )

    response = session.get('https://ordermanagement.unfi.com/api/Categories/GetCategoriesOrderByDepartments',
                           headers=headers, params=params)


def get_categories_by_brand_id(session, token, brand_id, cust_num):
    headers = {
        'authority': 'order_management.unfi.com',
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


def get_products_by_category_id():
    import requests

    headers = {
        'authority': 'ordermanagement.unfi.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'authorization': '155329~2261350b-fe77-486b-aed5-d09a5c6af64e:77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+MDUudHx1bmZpc3RzfGJ1bGtAY2FwZWxsYW1hcmtldC5jb20sMDUudHx1bmZpc3RzfGJ1bGtAY2FwZWxsYW1hcmtldC5jb20sMTMyMjkxMTg1MzEyMTczODEzLEZhbHNlLG0wNjRRT1d0OGQ4VzhyVGFRQVo5ckxFbmVId3FFdVJPNzB0ZTRDemxLRE51RkxONW5QeUFocTQvK1N4QlhRM2Z3T0NDSkM2VUIrNjlsOC9nYmM1UWo5TGxjSWN1TldwR1RtM0dSaEFLRU10emxoNkZxQm82NVpRSzd3cWlIZ3YwZmZDeFE5UmxXbUhZRnh6bEx1T1J5VUtucVZQaU1rSHEzRExiTTVYR0o0bSs2eFhOeDJRZmhnSCtKNXhLUmtMRER0d1duMnVIZXVsRm16SGVodUZmbUF2dFBWR2hYZUJvWG1tVDlPeDh0Yk1EcjlJQnJNOEg0UkxkUW1uYzUxZXZCMUszMGF0MnBncDdqaEdVUFhqRFVZSG9sTVRYTWtMMnoxZzIrY1ZhZlB5bm1hNThCUnVQYmVSZm9TaFoyTUErSDYxaDdQRSs1YVZpdUQySnRhWnFBUT09LGh0dHBzOi8vY3VzdG9tZXJzLnVuZmkuY29tLzwvU1A+:1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'dnt': '1',
        'origin': 'https://customers.unfi.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'referer': 'https://customers.unfi.com/Pages/CategoryDetail.aspx?categoryId=636&categoryName=NON%20FOODS%20-%20PAPER%20%26%20PICNIC',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('brandId', ''),
        ('region', 'West'),
        ('accountNumber', '001014    '),
        ('userId', '155329'),
        ('warehouse', '6'),
        ('sortOrder', 'BrandName'),
        ('sortDescription', 'ASC'),
        ('categoryId', '636'),
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
        ('pageSize', '5000'),
        ('pageNumber', '1'),
        ('type', 'category'),
        ('isPrivateLabel', 'false'),
    )

    response = requests.get('https://ordermanagement.unfi.com/api/Categories/GetProductsByCategoryId', headers=headers,
                            params=params)
    return response_to_json(response)
    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://ordermanagement.unfi.com/api/Categories/GetProductsByCategoryId?brandId=&region=West&accountNumber=001014++++&userId=155329&warehouse=6&sortOrder=BrandName&sortDescription=ASC&categoryId=636&categoryName=&brandName=&productType=&upc=&productCode=&productDescription=&brandIds=&categoryIds=&allWords=&atLeastOneWord=&exactPhrase=&excludeWords=&searchProductInProductDescription=&searchProductInProductIngredients=&searchProductInAdditionalInfo=&searchProductInProductAttributes=&isAdminOrAccountManager=true&pageSize=50&pageNumber=1&type=category&isPrivateLabel=false', headers=headers)
