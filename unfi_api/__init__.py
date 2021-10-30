# __all__ = ['UnfiAPI', 'product', 'api', 'invoice']
from unfi_api.api.api import UnfiAPI
from unfi_api.api.base_classes import APICore
from unfi_api.api.response import APIResponse, NonJsonResultError
from unfi_api.search.result import Result
from unfi_api.product.pricing import Pricing


class UnfiApiClient:
    def __init__(self, api: APICore):
        self.api = api

    def search(
        self,
        query,
        limit=1000,
        organic_codes="",
        attribute_ids="",
        sales_filters="",
        brand_ids="",
        category_ids="",
        page_number=1,
    ):
        result = self._order_management.brands.get_products_by_full_text(
            query,
            limit,
            organic_codes,
            attribute_ids,
            sales_filters,
            brand_ids,
            category_ids,
            page_number,
        )
        res = Result.parse_obj(result["data"])
        return res

    def get_pricing(self, product_code: str) -> Pricing:

        response: APIResponse = (
            self._order_management.brands.get_product_pricing_detail(product_code)
        )
        if not response.data:
            raise NonJsonResultError(
                f"Non-JSON API response for product code {product_code}"
            )
        res = Pricing.parse_obj(response.data)
        return res


def main():
    client = UnfiApiClient("capellaAPI", "CapellaAPI2489", incapusla=False)
    result = client.search("chocolate")
    pass


if __name__ == "__main__":
    main()
