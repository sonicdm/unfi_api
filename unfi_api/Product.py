import json

import requests
from bs4 import BeautifulSoup

from .utils import strings_to_numbers, simple_round_retail
from .utils.upc import stripcheckdigit
from unfi_api.settings import xdock_cust_num, ridgefield_cust_num, product_data_url, product_detail_url, user_id, \
    promo_url, product_attribute_url, api_thread_limit
from unfi_api.tools import combine_dicts, Threading


def get_attributes(product_id, header):
    result = fetch_attributes_from_api(product_id, header)
    out = parse_attributes(result)
    return out


def fetch_attributes_from_api(product_id, header):
    """
    Query the API for the attributes of a product_id.
    :param product_id:
    :param header:
    :return:
    """
    attribute_url = product_attribute_url.format(product_id=product_id)
    attribute_response = requests.get(attribute_url, header)
    attribute_result = json.loads(attribute_response.content)
    return attribute_result


def parse_attributes(result):
    """
    break out the attribute names and flag them as present
    :param result:  json result of attributes
    :return: dict of attribute flags
    """
    return {r["AttributeName"]: "Y" for r in result}


def product_info(product_list, token, xdock=False):
    """
    Take a search result and turn it into a list of products and their metadata.
    Will return a dict of all of the possible fields from the combined dicts.
    :param product_list:
    :param xdock:
    :return:
    """
    products = {}
    i = 1
    threading = Threading(max_workers=api_thread_limit)
    products['fields'] = []

    def _compile_product(product):
        upc = strings_to_numbers(stripcheckdigit(product['UPC']))
        product_id = product['ProductIntID']
        product_code = product['ProductCode']
        p = get_product_info(product_id, product_code, token, xdock)
        # get the product listing part of the search result
        p['listing'] = product
        md = combine_dicts(*p.values())
        md['upc_no_check'] = upc
        if xdock:
            md['xdock'] = "Y"
        products['fields'].extend(md.keys())
        products[upc] = md

    threading.thread_with_progressbar(_compile_product, product_list)
    products['fields'] = set([f for f in products['fields']])
    return products


def pull_main_data(product_code, custnum, header):
    # Pulling the main data
    data_url = product_data_url.format(product_code=product_code, custnum=custnum)
    data_response = requests.get(data_url, headers=header)
    data_result = json.loads(data_response.content)
    return data_result


def fetch_product_detail_from_api(product_id, custnum, user_id, header):
    # Pulling the extra details
    detail_url = product_detail_url.format(product_id=product_id, custnum=custnum, userid=user_id)
    detail_response = requests.get(detail_url, headers=header)
    detail_result = json.loads(detail_response.content).pop()
    return detail_result


def get_pricing(custnum, product_code, header):
    response = fetch_pricing_from_api(custnum, product_code, header)
    pricing = parse_pricing(response)
    return pricing


def fetch_pricing_from_api(custnum, product_code, header):
    # pulling the detailed pricing. Ensures the retail price is not a promo price.
    promoprice_url = promo_url.format(custnum=custnum, product_code=product_code)
    promotion_response = requests.get(promoprice_url, headers=header)
    return promotion_response.content


def parse_pricing(response_content):
    promo_soup = BeautifulSoup(response_content, 'html.parser')
    # find table that contains the pricing.
    promo_table = promo_soup.find_all('table')[1]
    promo_rows = []
    promo_headers = [header.text for header in promo_table.find_all('th')]
    promo_rows.append(promo_headers)
    # grab table values and put into lists
    for row in promo_table.find_all('tr'):
        cur_row = []
        for cell in row.find_all('td'):
            cur_row.append(cell.get_text().replace('\\r', '').replace('\\t', '').replace('\\n', '').strip())
        promo_rows.append(cur_row)
    promo_rows.remove([])

    # create pricing data
    pricing = {}

    for row in promo_rows[1:]:
        row = [strings_to_numbers(str(i).replace('$', '')) for i in row]
        price_type = row[0]
        if not price_type:
            pricing['retail_case_cost'] = row[-4]
            pricing['retail_unit_cost'] = row[-3]
            pricing['retail_srp'] = simple_round_retail(row[-2])
            continue
        else:
            promo_price = row[-2]
            promo_case_cost = row[9]
            promo_unit_cost = row[10]
            promo_from = row[7]
            promo_to = row[8]
            promo_key = price_type + "_"
            pricing[promo_key + "srp"] = promo_price
            pricing[promo_key + "case_cost"] = promo_case_cost
            pricing[promo_key + "unit_cost"] = promo_unit_cost
            pricing[promo_key + "from"] = promo_from
            pricing[promo_key + "to"] = promo_to

    return pricing


def get_product_info(product_id, product_code, token, xdock=False, callback=None):
    """
    Query and find all metadata for a given product.
    :param product_id:
    :param product_code:
    :param token:
    :param xdock:
    :return:
    """
    header = {
        'authorization': '{token}'.format(token=token, )
    }

    if xdock:
        custnum = xdock_cust_num
    else:
        custnum = ridgefield_cust_num
    data_result = pull_main_data(product_code, custnum, header)
    detail_result = fetch_product_detail_from_api(product_id, custnum, user_id, header)
    attribute_result = get_attributes(product_id, header)
    detail_result.update(attribute_result)
    pricing = get_pricing(custnum, product_code, header)

    product = {"detail": detail_result, "data": data_result, 'pricing': pricing}
    return product
