
from .products import get_product_by_int_id, get_product_attributes, get_product_data

class Products(object):
    """

    :type api: `unfi_api.api.UnfiAPI`
    """

    def __init__(self, api):
        self.api = api
        pass

    def get_product_by_int_id(self, product_int_id):
        result = get_product_by_int_id(self.api.auth_token, product_int_id)
        return result