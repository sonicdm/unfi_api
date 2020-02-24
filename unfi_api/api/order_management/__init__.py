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

        return brands.get_products_by_full_text(self.api.auth_token, query, account_number, user_id,
                                                region, warehouse)



    get_products_by_full_text.__doc__ = brands.get_products_by_full_text.__doc__


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
