import re
from urllib import parse

from bs4 import BeautifulSoup
from pydantic.class_validators import root_validator, validator
from unfi_api.invoice import Invoice, get_invoice_html_tables, get_table_data
from unfi_api.api.api import Endpoint, APICore

from unfi_api.api.response import APIResponse
from ...utils.string import strings_to_numbers
from unfi_api.utils.http import response_to_api_response, response_to_json
from . import brands, categories, interactive_reports, order_history, product_detail
from unfi_api import settings

order_history_base_url = 'https://ordermanagement.unfi.com/api/OrderHistory/'


class OrderManagement(Endpoint):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.api: APICore = api
        self.brands = Brands(api)
        self.categories = Categories(api)
        self.order_history = OrderHistory(api)
        self.product_detail = ProductDetail(api)
        self.interactive_reports = InteractiveReports(api)
        pass


class Brands(Endpoint):
    """
    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.api: APICore = api
        pass

    def get_products_by_full_text(self, query, limit=1000, organic_codes='', attribute_ids='', sales_filters='',
                                  brand_ids='', category_ids='', page_number=1, **kwargs):
        token = self.api.auth_token
        account_number = self.api.account
        user_id = self.api.user_id
        region = self.api.account_region
        warehouse = self.api.warehouse,

        return brands.get_products_by_full_text(self.api.session, token, query, account_number, user_id,
                                                region, warehouse)

    def get_brands(self, page_size=9999, page_number=1, brand_prefix='A', **kwargs):
        token = self.api.auth_token
        region = self.api.account_region
        warehouse = self.api.warehouse,
        account_number = self.api.account

        return brands.get_brands(self.api.session, token, region, warehouse, account_number, page_size=page_size,
                                 page_number=page_number,
                                 brand_prefix=brand_prefix, **kwargs)

    def get_products_by_brand_id(self, brand_id, sort_order='ASC', sort_description="BrandName", category_id='',
                                 category_name='', brand_name='', product_type='', upc='', product_code='',
                                 product_description='', brand_ids='', category_ids='', all_words='',
                                 at_least_one_word='', exact_phrase='', exclude_words='',
                                 search_product_in_product_description='', search_product_in_product_ingredients='',
                                 search_product_in_product_attribbutes='', search_product_in_additional_info='',
                                 page_size=1000, page_number=1, _type='brand', is_private_label='false'):
        token = self.api.auth_token
        region = self.api.account_region
        warehouse = self.api.warehouse,
        account_number = self.api.account
        user_id = self.api.user_id
        return brands.get_products_by_brand_id(self.api.session,
                                               token, account_number, user_id, warehouse, region, brand_id,
                                               sort_order,
                                               sort_description, category_id, category_name,
                                               brand_name,
                                               product_type, upc, product_code, product_description,
                                               brand_ids,
                                               category_ids, all_words, at_least_one_word, exact_phrase,
                                               exclude_words,
                                               search_product_in_product_description,
                                               search_product_in_product_ingredients,
                                               search_product_in_product_attribbutes,
                                               search_product_in_additional_info,
                                               page_size, page_number, _type, is_private_label
                                               )

    def get_product_pricing_detail(self, product_code):
        return brands.get_product_details_from_service(self.api.session, self.api.auth_token, product_code,
                                                       self.api.account)


class Categories(Endpoint):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.api: APICore = api
        pass


class InteractiveReports(Endpoint):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.api: APICore = api
        pass

    def get_products_by_top_sellers(self, start_date=None, end_date=None,
                                    brand_id='', sort_order='QuantitySold', sort_description='DESC', category_id='',
                                    category_name='', brand_name='', product_type='', upc='', product_code='',
                                    product_description='', brand_ids='', category_ids='', all_words='',
                                    at_least_one_word='', exact_phrase='', exclude_words='',
                                    search_product_in_product_description='', search_product_in_product_ingredients='',
                                    search_product_in_additional_info='', search_product_in_product_attributes='',
                                    is_admin_or_account_manager='true', page_size=50, page_number=1, _type='TopSellers',
                                    is_private_label='false', department_id='', top_rank='', apply_channel='',
                                    **kwargs):
        # token, account_number, user_id, region, warehouse,
        result = interactive_reports.get_products_by_top_sellers(self.api.session,
                                                                 self.api.auth_token, self.api.account,
                                                                 self.api.user_id, self.api.account_region,
                                                                 self.api.warehouse, start_date, end_date,
                                                                 brand_id, sort_order, sort_description, category_id,
                                                                 category_name, brand_name, product_type, upc,
                                                                 product_code, product_description, brand_ids,
                                                                 category_ids, all_words, at_least_one_word,
                                                                 exact_phrase,
                                                                 exclude_words, search_product_in_product_description,
                                                                 search_product_in_product_ingredients,
                                                                 search_product_in_additional_info,
                                                                 search_product_in_product_attributes,
                                                                 is_admin_or_account_manager,
                                                                 page_size, page_number, _type, is_private_label,
                                                                 department_id, top_rank, apply_channel, **kwargs,

                                                                 )

        return result


class InvoiceResponse(APIResponse):

    @root_validator(pre=True)
    def __get_table_data(cls, values):
        values['data'] = get_invoice_html_tables(values['text'])
        return values


class OrderHistory(Endpoint):
    """

    """

    def __init__(self, api: APICore):
        self.api: APICore = api
        pass

    def get_invoice_list(self, order_no=None, po_no=None, req_by=None, invoice_no=None,
                         page_size=1000, page_number=1, sort_expression=None, sort_direction=None):
        response = order_history.get_grid_item(self.api.session, self.api.auth_token, self.api.account, self.api.user_id,
                                           self.api.account_region, transaction_type=1)

        return response

    def get_credit_list(self, order_no=None, po_no=None, req_by=None, invoice_no=None,
                        page_size=1000, page_number=1, sort_expression=None, sort_direction=None):
        return order_history.get_grid_item(self.api, self.api.auth_token, self.api.account, self.api.user_id,
                                           self.api.account_region, transaction_type=4)

    def get_invoice(self, invoice_number, command=''):
        """
        "https://ordermanagement.unfi.com/api/OrderHistory/
        GetCreditInvoiceDetailForWest?invoiceNumber={invoicenum}&customerNumber={custnum}&command="
        """

        endpoint = "GetCreditInvoiceDetailForWest"
        url = order_history_base_url + endpoint

        params = (
            ('invoiceNumber', invoice_number),
            ('customerNumber', self.api.account.strip()),
            ('command', command),
        )

        response = self.api.get(
            'https://ordermanagement.unfi.com/api/OrderHistory/GetCreditInvoiceDetailForWest', params=params
        )

        error = None

        data = None
        result = response_to_api_response(response, InvoiceResponse)
        # data = get_table_data(result.text)
        # result.data = data
        # result = {
        #     "error": error,
        #     "status": response.status_code,
        #     "data": data,
        #     "content": response.content,
        #     "response": response
        # }
        return result


product_detail_endpoint = 'https://ordermanagement.unfi.com/api/ProductDetail/'


class ProductDetail(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api: APICore):
        self.api: APICore = api
        pass

    def get_product_detail_by_int_id(self, product_int_id):
        header = {
            'authorization': self.api.auth_token
        }
        endpoint_name = "GetProductDetailByProductIntId"
        url = parse.urljoin(product_detail_endpoint, endpoint_name)
        params = {
            'productIntId': product_int_id,
            'region': self.api.account_region,
            'accountNumber': self.api.account.strip(),
            'warehouse': self.api.warehouse_id,
            'userId': self.api.user_id
        }

        result = self.api.get(url, headers=header, params=params)
        return response_to_json(result)


def parse_invoice_html_to_json(page):
    no_lines = "<html><body>" + re.sub(r"(\r|\t|\n)+", " ", page) + "</body></html>"
    no_lines = re.sub(r"((\\r)+|(\\t)+|(\\n)+)", "", no_lines)
    invoicesoup = BeautifulSoup(no_lines, features=settings.beautiful_soup_parser)

    # invoice metadata eg invoice number and such
    meta = {}
    meta_table = invoicesoup.find('td', text=re.compile(r"(Invoice|Credit) Number")).find_parent('tbody')
    meta_table_rows = [x.find_all('td') for x in meta_table.find_all("tr")]
    meta_headers = [x.text.strip() for x in meta_table_rows[0]]
    meta = {meta_headers[i]: x.text.strip() for i, x in enumerate(meta_table_rows[1])}

    # products on the invoice.
    remarks = {}
    line_items = {}
    line_items_table = invoicesoup.find('td', text=re.compile(r"Product Code")).find_parent('tbody')
    line_item_rows = [x.find_all('td') for x in line_items_table.find_all("tr")]
    line_item_headers = [x.text.strip() for x in line_item_rows[0]]
    for row in line_item_rows[1:]:
        line_item = {}
        for idx, td in enumerate(row):
            line_item[line_item_headers[idx]] = strings_to_numbers(td.text.strip())
        if line_item["Product Code"] == "REMRK":
            remarks[line_item["LN"]] = line_item
        else:
            line_items[line_item['LN']] = line_item

    # freight detail
    freight = {}
    freight_table = invoicesoup.find('b', text=re.compile(r"Freight Details")).find_parent("tbody")
    for tr in list(freight_table.find_all('tr'))[1:]:
        k, v = [td.text for td in tr.find_all('td')]
        freight[k] = v

    # Invoice Summary
    invoice_summary = {}
    invoice_table = invoicesoup.find('b', text=re.compile(r"Invoice Summary")).find_parent("tbody")
    for tr in list(invoice_table.find_all('tr'))[1:]:
        k, v = [td.text for td in tr.find_all('td')]
        invoice_summary[k] = v

    shipping_table = invoicesoup.find('b', text=re.compile(r"Shipping")).find_parent("tbody")
    shipping = {}
    address_keys = []
    address_values = []
    for tr in list(shipping_table.find_all('tr'))[1:]:
        k, v = [x.text for x in tr.find_all('td')]
        address_keys.append(k.strip())
        address_values.append(v.strip())

    to_start = address_keys.index("To:")
    to_stop = address_keys.index("Address:")
    shipping['to'] = " ".join(address_values[to_start:to_stop])
    add_start = address_keys.index("Address:")
    add_end = address_keys.index("City:")
    shipping['address'] = " ".join(address_values[add_start:add_end])
    shipping['city'] = address_values[address_keys.index("City:")]
    shipping['state'] = address_values[address_keys.index("State:")]
    shipping['zipcode'] = address_values[address_keys.index("Zip Code:")]

    invoice = {
        "details": meta,
        "items": line_items,
        "remarks": remarks,
        "to": shipping,
        "invoice_summary": invoice_summary,
        "freight_details": freight
    }
    return invoice
