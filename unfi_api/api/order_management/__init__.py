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


class OrderHistory(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
        pass
