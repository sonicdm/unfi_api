from . import brands, categories, interactive_reports, order_history


class OrderManagement(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
        self.brands = Brands(api)
        self.categories = Categories(api)
        self.interactive_reports = InteractiveReports(api)
        self.order_history = OrderHistory(api)
        self.product_detail = ProductDetail(api)
        pass


class Brands(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
        pass

    def get_products_by_full_text(self, query, limit=1000, organic_codes='', attribute_ids='', sales_filters='',
                                  brand_ids='', category_ids='', page_number=1, **kwargs):
        token = self.api.auth_token
        account_number = self.api.account
        user_id = self.api.user_id
        region = self.api.account_region
        warehouse = self.api.warehouse,

        return brands.get_products_by_full_text(token, query, account_number, user_id,
                                                region, warehouse)

    def get_brands(self, page_size=9999, page_number=1, brand_prefix='A', **kwargs):
        token = self.api.auth_token
        region = self.api.account_region
        warehouse = self.api.warehouse,
        account_number = self.api.account

        return brands.get_brands(token, region, warehouse, account_number, page_size=page_size, page_number=page_number,
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
        return brands.get_products_by_brand_id(
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


class Categories(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
        pass


class InteractiveReports(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
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
        result = interactive_reports.get_products_by_top_sellers(
            self.api.auth_token, self.api.account, self.api.user_id, self.api.account_region, self.api.warehouse, start_date, end_date,
            brand_id, sort_order, sort_description, category_id, category_name, brand_name, product_type, upc,
            product_code, product_description, brand_ids, category_ids, all_words, at_least_one_word, exact_phrase,
            exclude_words, search_product_in_product_description, search_product_in_product_ingredients,
            search_product_in_additional_info, search_product_in_product_attributes, is_admin_or_account_manager,
            page_size, page_number, _type, is_private_label, department_id, top_rank, apply_channel, **kwargs,

        )

        return result


class OrderHistory(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
        pass

    def get_invoice_list(self, order_no=None, po_no=None, req_by=None, invoice_no=None,
                         page_size=1000, page_number=1, sort_expression=None, sort_direction=None):
        return order_history.get_grid_item(self.api.auth_token, self.api.account, self.api.user_id,
                                           self.api.account_region, transaction_type=1)


class ProductDetail(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
        pass
