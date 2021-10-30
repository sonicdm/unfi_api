from unfi_api.api import UnfiAPI
from unfi_api.search.result import Result

class UnfiApiClient(UnfiAPI):
    def __init__(self, user, password, incapusla=True, incapsula_retry=False, incapsula_retry_limit=10):
        super().__init__(user, password, incapusla, incapsula_retry, incapsula_retry_limit)

    def search(self, query, limit=1000, organic_codes='', attribute_ids='', sales_filters='', brand_ids='', category_ids='', page_number=1):
        result = self._order_management.brands.get_products_by_full_text(
            query, limit, organic_codes, attribute_ids, sales_filters, brand_ids, category_ids, page_number
        )
        
        return Result.parse_obj(result['data'])

