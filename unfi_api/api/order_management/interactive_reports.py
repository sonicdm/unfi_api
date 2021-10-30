import requests
import urllib.parse
from dateutil import parser
import json

from datetime import date, datetime, timedelta
from unfi_api.utils.http import response_to_json
from unfi_api.utils.date import fuzzy_date

"""
'https://ordermanagement.unfi.com/api/InteractiveReports/
"""
endpoint = r'https://ordermanagement.unfi.com/api/InteractiveReports/'


def get_products_by_top_sellers(session, token, account_number, user_id, region, warehouse, start_date=None,
                                end_date=None,
                                brand_id='', sort_order='QuantitySold', sort_description='DESC', category_id='',
                                category_name='', brand_name='', product_type='', upc='', product_code='',
                                product_description='', brand_ids='', category_ids='', all_words='',
                                at_least_one_word='', exact_phrase='', exclude_words='',
                                search_product_in_product_description='', search_product_in_product_ingredients='',
                                search_product_in_additional_info='', search_product_in_product_attributes='',
                                is_admin_or_account_manager='true', page_size=50, page_number=1, _type='TopSellers',
                                is_private_label='false', department_id='', top_rank='', apply_channel='', **kwargs):
    """
    Parameter defaults
        'sortOrder': 'QuantitySold',
        'sortDescription': 'DESC',
        'isAdminOrAccountManager': 'true',
        'pageSize': '50',
        'pageNumber': '1',
        'type': 'TopSellers',
        'isPrivateLabel': 'false',
        'startDate': 30 days before endDate,
        'endDate': 'today',
        'topRank': '50'
    """
    date_format = "%m/%d/%Y"
    if start_date:
        if not isinstance(start_date, (str, date, datetime)):
            raise ValueError("start_date must be type str, date, or datetime")
        if isinstance(start_date, str):
            start_date = parser.parse(start_date, fuzzy=True).date()
        elif isinstance(start_date, datetime):
            start_date = start_date.date()
        if not (end_date):
            end_date = date.today()
    elif end_date:
        if not isinstance(end_date, (str, date, datetime)):
            raise ValueError("end_date must be type str, date, or datetime")
        if isinstance(end_date, str):
            end_date = parser.parse(end_date, fuzzy=True).date()
        elif isinstance(end_date, datetime):
            end_date = end_date.date()
        if not start_date:
            start_date = end_date - timedelta(days=30)
    else:
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

    end_date_str = end_date.strftime(date_format)
    start_date_str = start_date.strftime(date_format)

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
        'brandId': brand_id,
        'region': region,
        'accountNumber': account_number,
        'userId': user_id,
        'warehouse': warehouse,
        'sortOrder': sort_order,
        'sortDescription': sort_description,
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
        'searchProductInProductAttributes': search_product_in_product_attributes,
        'isAdminOrAccountManager': is_admin_or_account_manager,
        'pageSize': page_size,
        'pageNumber': page_number,
        'type': _type,
        'isPrivateLabel': is_private_label,
        'departmentId': department_id,
        'startDate': start_date_str,
        'endDate': end_date_str,
        'topRank': top_rank,
        'applyChannel': apply_channel,
    }
    params.update(**kwargs)
    echo_url = "http://localhost:8000"
    response = session.get(url, headers=headers, params=params)
    return response_to_json(response)
