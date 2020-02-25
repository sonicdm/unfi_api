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